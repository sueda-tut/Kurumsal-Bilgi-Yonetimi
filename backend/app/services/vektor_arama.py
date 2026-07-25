# Soruları embedding'e dönüştürerek yetki filtreli pgvector benzerlik araması yapar

from dataclasses import dataclass

from pgvector.sqlalchemy import Vector
from sqlalchemy import Integer, bindparam, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ai.embeddings import (
    EmbeddingUretmeHatasi,
    embeddingleri_uret,
)
from app.models.kullanici import Kullanici
from app.services.dokuman_yetki import (
    gorebildigi_dokuman_idleri,
)


VARSAYILAN_SONUC_SAYISI = 5
MAKSIMUM_SONUC_SAYISI = 20


@dataclass(frozen=True, slots=True)
class VektorAramaSonucu:
    parca_id: int
    dokuman_id: int
    parca_sirasi: int
    parca_metni: str
    sayfa_no: int | None
    baslik: str
    benzerlik_puani: float


class VektorAramaHatasi(Exception):
    """Yetki filtreli vektör araması başarısız olduğunda oluşur."""


# Benzerlik ve doküman yetkisini aynı SQL sorgusunda uygular
VEKTOR_ARAMA_SQL = text(
    """
    SELECT
        dp.parca_id,
        dp.dokuman_id,
        dp.parca_sirasi,
        dp.parca_metni,
        dp.sayfa_no,
        d.baslik,
        1 - (dp.embedding <=> :soru_vektor)
            AS benzerlik_puani
    FROM dokuman_parcalari AS dp
    JOIN dokumanlar AS d
        ON d.dokuman_id = dp.dokuman_id
    WHERE
        dp.embedding IS NOT NULL
        AND LOWER(d.durum) = 'aktif'
        AND dp.dokuman_id IN :dokuman_idleri
    ORDER BY dp.embedding <=> :soru_vektor
    LIMIT :sonuc_limiti
    """
).bindparams(
    bindparam(
        "soru_vektor",
        type_=Vector(1536),
    ),
    bindparam(
        "dokuman_idleri",
        expanding=True,
    ),
    bindparam(
        "sonuc_limiti",
        type_=Integer,
    ),
)


def ilgili_parcalari_ara(
    db: Session,
    kullanici: Kullanici,
    soru: str,
    limit: int = VARSAYILAN_SONUC_SAYISI,
) -> list[VektorAramaSonucu]:
    """
    Soruyu embedding'e dönüştürür ve yalnızca kullanıcının
    görebildiği dokümanlarda cosine benzerlik araması yapar.
    """

    temiz_soru = soru.strip()

    if not temiz_soru:
        raise ValueError("Arama sorusu boş olamaz.")

    if not 1 <= limit <= MAKSIMUM_SONUC_SAYISI:
        raise ValueError(
            "Sonuç limiti 1 ile 20 arasında olmalıdır."
        )

    gorulebilir_idler = gorebildigi_dokuman_idleri(
        db=db,
        kullanici=kullanici,
    )

    if not gorulebilir_idler:
        return []

    try:
        soru_vektoru = embeddingleri_uret(
            [temiz_soru]
        )[0]

        satirlar = db.execute(
            VEKTOR_ARAMA_SQL,
            {
                "soru_vektor": soru_vektoru,
                "dokuman_idleri": gorulebilir_idler,
                "sonuc_limiti": limit,
            },
        ).mappings().all()

    except EmbeddingUretmeHatasi as hata:
        raise VektorAramaHatasi(
            "Soru embedding'i üretilemedi."
        ) from hata

    except SQLAlchemyError as hata:
        raise VektorAramaHatasi(
            "PostgreSQL vektör araması gerçekleştirilemedi."
        ) from hata

    return [
        VektorAramaSonucu(
            parca_id=satir["parca_id"],
            dokuman_id=satir["dokuman_id"],
            parca_sirasi=satir["parca_sirasi"],
            parca_metni=satir["parca_metni"],
            sayfa_no=satir["sayfa_no"],
            baslik=satir["baslik"],
            benzerlik_puani=float(
                satir["benzerlik_puani"]
            ),
        )
        for satir in satirlar
    ]