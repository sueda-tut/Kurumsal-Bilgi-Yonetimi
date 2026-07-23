# Sohbet oturumu ve mesaj endpoint'lerini kullanıcı sahipliğiyle korur

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.crud.sohbet import (
    kullanicinin_oturumlarini_listele,
    oturumun_mesajlarini_listele,
    sohbet_mesaji_olustur,
    sohbet_oturumu_getir,
    sohbet_oturumu_olustur,
)
from app.db.database import get_db
from app.models.kullanici import Kullanici
from app.models.sohbet_oturumu import SohbetOturumu
from app.schemas.sohbet_mesaji import (
    MesajGonderRequest,
    SohbetMesajiResponse,
)
from app.schemas.sohbet_oturumu import (
    SohbetOlusturRequest,
    SohbetOturumuResponse,
)


router = APIRouter(
    prefix="/sohbetler",
    tags=["Sohbetler"],
)


# Oturumun varlığını ve token sahibine ait olduğunu kontrol eder
def kullanicinin_sohbetini_getir(
    db: Session,
    oturum_id: int,
    current_user: Kullanici,
) -> SohbetOturumu:
    oturum = sohbet_oturumu_getir(
        db=db,
        oturum_id=oturum_id,
    )

    if oturum is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sohbet oturumu bulunamadı.",
        )

    if oturum.kullanici_id != current_user.kullanici_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bu sohbet oturumuna erişim yetkiniz yok.",
        )

    return oturum


# Token sahibi kullanıcı için yeni sohbet oturumu açar
@router.post(
    "",
    response_model=SohbetOturumuResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni sohbet oturumu aç",
)
def yeni_sohbet_olustur(
    sohbet_verisi: SohbetOlusturRequest,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    if not sohbet_verisi.oturum_basligi.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Oturum başlığı boş olamaz.",
        )

    return sohbet_oturumu_olustur(
        db=db,
        kullanici_id=current_user.kullanici_id,
        oturum_basligi=sohbet_verisi.oturum_basligi,
    )


# Token sahibi kullanıcının kendi sohbetlerini listeler
@router.get(
    "",
    response_model=list[SohbetOturumuResponse],
    summary="Kendi sohbet oturumlarını listele",
)
def sohbetleri_listele(
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    return kullanicinin_oturumlarini_listele(
        db=db,
        kullanici_id=current_user.kullanici_id,
    )


# Token sahibinin belirtilen oturumdaki mesajlarını getirir
@router.get(
    "/{oturum_id}",
    response_model=list[SohbetMesajiResponse],
    summary="Sohbet mesajlarını getir",
)
def sohbet_mesajlarini_getir(
    oturum_id: int,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    kullanicinin_sohbetini_getir(
        db=db,
        oturum_id=oturum_id,
        current_user=current_user,
    )

    return oturumun_mesajlarini_listele(
        db=db,
        oturum_id=oturum_id,
    )


# Token sahibinin kendi sohbet oturumuna mesaj eklemesini sağlar
@router.post(
    "/{oturum_id}/mesaj",
    response_model=SohbetMesajiResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Sohbet oturumuna mesaj ekle",
)
def sohbet_mesaji_ekle(
    oturum_id: int,
    mesaj_verisi: MesajGonderRequest,
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    kullanicinin_sohbetini_getir(
        db=db,
        oturum_id=oturum_id,
        current_user=current_user,
    )

    if not mesaj_verisi.mesaj_metni.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Mesaj metni boş olamaz.",
        )

    return sohbet_mesaji_olustur(
        db=db,
        oturum_id=oturum_id,
        mesaj_metni=mesaj_verisi.mesaj_metni,
    )