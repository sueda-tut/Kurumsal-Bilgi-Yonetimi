# Dokümanı çıkarma, parçalama, embedding üretme ve kaydetme adımlarıyla işler

from pathlib import Path

from sqlalchemy.orm import Session

from ai.chunking import bolumleri_parcalara_ayir
from ai.embeddings import (
    EmbeddingUretmeHatasi,
    embeddingleri_uret,
)
from ai.extractors import (
    MetinCikarmaHatasi,
    dosyadan_metin_cikar,
)
from app.crud.dokuman_parcasi import (
    dokuman_parcalarini_kaydet,
)
from app.models.dokuman import Dokuman
from app.models.dokuman_parcasi import DokumanParcasi


class DokumanIslemeHatasi(Exception):
    """Doküman işleme adımlarından biri başarısız olduğunda oluşur."""


def dokumani_isle(
    db: Session,
    dokuman: Dokuman,
    fiziksel_dosya_yolu: str | Path,
) -> list[DokumanParcasi]:
    """
    Dokümandan metin çıkarır, chunk oluşturur, embedding
    üretir ve tamamını PostgreSQL'e kaydeder.
    """

    try:
        # 1. Dosyadan temiz metin çıkarır
        bolumler = dosyadan_metin_cikar(
            fiziksel_dosya_yolu
        )

        if not bolumler:
            raise DokumanIslemeHatasi(
                "Dosyadan okunabilir metin çıkarılamadı."
            )

        # 2. Metni yaklaşık 600 tokenlık parçalara ayırır
        parcalar = bolumleri_parcalara_ayir(bolumler)

        if not parcalar:
            raise DokumanIslemeHatasi(
                "Doküman parçaları oluşturulamadı."
            )

        # 3. Her parça için OpenAI embedding üretir
        embeddingler = embeddingleri_uret(
            [
                parca.parca_metni
                for parca in parcalar
            ]
        )

        # 4. Parçaları ve vektörleri PostgreSQL'e kaydeder
        return dokuman_parcalarini_kaydet(
            db=db,
            dokuman=dokuman,
            parcalar=parcalar,
            embeddingler=embeddingler,
        )

    except DokumanIslemeHatasi:
        raise

    except MetinCikarmaHatasi as hata:
        db.rollback()

        raise DokumanIslemeHatasi(
            "Dosyadan metin çıkarılamadı."
        ) from hata

    except EmbeddingUretmeHatasi as hata:
        db.rollback()

        raise DokumanIslemeHatasi(
            str(hata)
        ) from hata

    except Exception as hata:
        db.rollback()

        raise DokumanIslemeHatasi(
            "Doküman işlenirken beklenmeyen bir hata oluştu."
        ) from hata