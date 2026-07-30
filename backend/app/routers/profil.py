# Giriş yapan kullanıcının profil bilgilerini döndürür

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.departman import Departman
from app.models.kullanici import Kullanici
from app.schemas.profil import ProfilResponse


router = APIRouter(
    prefix="/profil",
    tags=["Profil"],
)


@router.get(
    "",
    response_model=ProfilResponse,
    summary="Giriş yapan kullanıcının profilini getirir",
)
def profil_getir(
    db: Session = Depends(get_db),
    current_user: Kullanici = Depends(get_current_user),
):
    departman_adi = db.scalar(
        select(Departman.departman_adi).where(
            Departman.departman_id
            == current_user.departman_id
        )
    )

    if departman_adi is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcının departmanı bulunamadı.",
        )

    return ProfilResponse(
        kullanici_id=current_user.kullanici_id,
        ad_soyad=current_user.ad_soyad,
        eposta=current_user.eposta,
        rol=current_user.rol,
        departman_id=current_user.departman_id,
        departman_adi=departman_adi,
        aktif_mi=current_user.aktif_mi,
    )