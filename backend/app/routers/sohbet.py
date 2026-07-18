# Kullanıcı oturumları ve oturum mesajları için GET endpoint'lerini tanımlar

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.crud.kullanici import kullanici_getir
from app.crud.sohbet import (
    kullanicinin_oturumlarini_listele,
    oturumun_mesajlarini_listele,
    sohbet_oturumu_getir,
)
from app.db.database import get_db
from app.schemas.sohbet_mesaji import (
    SohbetMesajiResponse,
)
from app.schemas.sohbet_oturumu import (
    SohbetOturumuResponse,
)


router = APIRouter(
    tags=["Sohbetler"],
)


@router.get(
    "/kullanicilar/{kullanici_id}/oturumlar",
    response_model=list[SohbetOturumuResponse],
)
def kullanicinin_oturumlari(
    kullanici_id: int,
    db: Session = Depends(get_db),
):
    kullanici = kullanici_getir(
        db=db,
        kullanici_id=kullanici_id,
    )

    if kullanici is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı.",
        )

    return kullanicinin_oturumlarini_listele(
        db=db,
        kullanici_id=kullanici_id,
    )


@router.get(
    "/oturumlar/{oturum_id}/mesajlar",
    response_model=list[SohbetMesajiResponse],
)
def oturumun_mesajlari(
    oturum_id: int,
    db: Session = Depends(get_db),
):
    oturum = sohbet_oturumu_getir(
        db=db,
        oturum_id=oturum_id,
    )

    if oturum is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sohbet oturumu bulunamadı.",
        )

    return oturumun_mesajlarini_listele(
        db=db,
        oturum_id=oturum_id,
    )