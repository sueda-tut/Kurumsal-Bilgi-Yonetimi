# Yetki filtreli RAG soru-cevap endpoint'ini oluşturur

import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ai.llm import (
    LlmCevapHatasi,
    kaynakli_cevap_uret,
)
from app.core.dependencies import get_current_user
from app.crud.mesaj_kaynagi import (
    mesaj_kaynagi_olustur,
)
from app.crud.sohbet import (
    sohbet_mesaji_kaydet,
    sohbet_oturumu_olustur,
)
from app.db.database import get_db
from app.models.kullanici import Kullanici
from app.routers.sohbet import (
    kullanicinin_sohbetini_getir,
)
from app.schemas.soru import (
    SoruKaynagiResponse,
    SoruRequest,
    SoruResponse,
)
from app.services.vektor_arama import (
    VektorAramaHatasi,
    ilgili_parcalari_ara,
)


logger = logging.getLogger(__name__)


router = APIRouter(
    tags=["RAG Soru-Cevap"],
)


# Soru metninden otomatik sohbet başlığı oluşturur
def otomatik_oturum_basligi_olustur(
    soru: str,
) -> str:
    temiz_soru = " ".join(soru.strip().split())

    if len(temiz_soru) <= 80:
        return temiz_soru

    return f"{temiz_soru[:77].rstrip()}..."


# Yeni veya mevcut sohbet oturumunun ID değerini belirler
def soru_oturumunu_hazirla(
    db: Session,
    soru_verisi: SoruRequest,
    current_user: Kullanici,
) -> int:
    if soru_verisi.oturum_id is not None:
        oturum = kullanicinin_sohbetini_getir(
            db=db,
            oturum_id=soru_verisi.oturum_id,
            current_user=current_user,
        )

        return oturum.oturum_id

    oturum_basligi = (
        soru_verisi.oturum_basligi.strip()
        if soru_verisi.oturum_basligi
        else otomatik_oturum_basligi_olustur(
            soru_verisi.soru
        )
    )

    yeni_oturum = sohbet_oturumu_olustur(
        db=db,
        kullanici_id=current_user.kullanici_id,
        oturum_basligi=oturum_basligi,
    )

    return yeni_oturum.oturum_id


# Soru, retrieval, LLM cevabı ve kaynak kayıtlarını tek akışta işler
@router.post(
    "/sor",
    response_model=SoruResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yetkili dokümanlara soru sor",
)
def soru_sor(
    soru_verisi: SoruRequest,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    temiz_soru = soru_verisi.soru.strip()

    if not temiz_soru:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Soru boş olamaz.",
        )

    oturum_id = soru_oturumunu_hazirla(
        db=db,
        soru_verisi=soru_verisi,
        current_user=current_user,
    )

    # Kullanıcı sorusunu sohbet mesajlarına kaydeder
    kullanici_mesaji = sohbet_mesaji_kaydet(
        db=db,
        oturum_id=oturum_id,
        gonderen_tipi="Kullanici",
        mesaj_metni=temiz_soru,
    )

    try:
        # Yalnızca kullanıcının görebildiği dokümanlarda arama yapar
        bulunan_parcalar = ilgili_parcalari_ara(
            db=db,
            kullanici=current_user,
            soru=temiz_soru,
            limit=5,
        )

        llm_cevabi = kaynakli_cevap_uret(
            soru=temiz_soru,
            parcalar=bulunan_parcalar,
        )

    except VektorAramaHatasi as hata:
        logger.exception(
            "Yetki filtreli vektör araması başarısız oldu."
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "Dokümanlarda arama yapılırken "
                "bir hata oluştu."
            ),
        ) from hata

    except LlmCevapHatasi as hata:
        logger.exception(
            "OpenAI üzerinden cevap üretilemedi."
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="AI cevabı üretilemedi.",
        ) from hata

    try:
        # AI mesajını önce flush ederek mesaj_id değerini alır
        ai_mesaji = sohbet_mesaji_kaydet(
            db=db,
            oturum_id=oturum_id,
            gonderen_tipi="AI",
            mesaj_metni=llm_cevabi.cevap,
            commit=False,
        )

        kaynak_cevaplari: list[
            SoruKaynagiResponse
        ] = []

        for kaynak_numarasi in (
            llm_cevabi.kullanilan_kaynak_numaralari
        ):
            parca = bulunan_parcalar[
                kaynak_numarasi - 1
            ]

            kaynak_kaydi = mesaj_kaynagi_olustur(
                db=db,
                mesaj_id=ai_mesaji.mesaj_id,
                parca_id=parca.parca_id,
                benzerlik_puani=parca.benzerlik_puani,
                commit=False,
            )

            kaynak_cevaplari.append(
                SoruKaynagiResponse(
                    kaynak_id=kaynak_kaydi.kaynak_id,
                    dokuman_id=parca.dokuman_id,
                    dokuman_basligi=parca.baslik,
                    parca_id=parca.parca_id,
                    parca_sirasi=parca.parca_sirasi,
                    sayfa_no=parca.sayfa_no,
                    benzerlik_puani=round(
                        parca.benzerlik_puani,
                        4,
                    ),
                )
            )

        db.commit()
        db.refresh(ai_mesaji)

    except SQLAlchemyError as hata:
        db.rollback()

        logger.exception(
            "AI mesajı veya mesaj kaynakları kaydedilemedi."
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                "AI cevabı veritabanına "
                "kaydedilemedi."
            ),
        ) from hata

    return SoruResponse(
        oturum_id=oturum_id,
        kullanici_mesaj_id=kullanici_mesaji.mesaj_id,
        ai_mesaj_id=ai_mesaji.mesaj_id,
        cevap=llm_cevabi.cevap,
        kaynaklar=kaynak_cevaplari,
    )