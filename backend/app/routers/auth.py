# Kullanıcı girişi ve token ile korunan deneme endpoint'ini oluşturur

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_HOURS,
    erisim_tokeni_olustur,
    sifre_dogrula,
)
from app.crud.kullanici import eposta_ile_kullanici_bul
from app.db.database import get_db
from app.models.kullanici import Kullanici
from app.schemas.auth import GirisRequest, TokenResponse
from app.schemas.kullanici import KullaniciResponse


router = APIRouter(tags=["Kimlik Doğrulama"])


# E-posta ve parola ile giriş yaparak JWT tokenı üretir
@router.post(
    "/giris",
    response_model=TokenResponse,
    summary="Kullanıcı girişi",
)
def giris_yap(
    giris_bilgileri: GirisRequest,
    db: Session = Depends(get_db),
):
    kullanici = eposta_ile_kullanici_bul(
        db=db,
        eposta=giris_bilgileri.eposta,
    )

    if kullanici is None or not sifre_dogrula(
        giris_bilgileri.sifre,
        kullanici.sifre_ozeti,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-posta veya şifre hatalı.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not kullanici.aktif_mi:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kullanıcı hesabı aktif değil.",
        )

    access_token = erisim_tokeni_olustur(
        kullanici_id=kullanici.kullanici_id
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_HOURS * 60 * 60,
    )


# Yalnızca geçerli tokenı bulunan kullanıcıların erişebildiği endpoint
@router.get(
    "/korumali-test",
    response_model=KullaniciResponse,
    summary="Token korumalı deneme endpoint'i",
)
def korumali_test(
    current_user: Kullanici = Depends(get_current_user),
):
    return current_user