# Kullanıcı kaydı, giriş işlemi ve token kontrol endpoint'lerini oluşturur

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.security import (
    ACCESS_TOKEN_EXPIRE_HOURS,
    erisim_tokeni_olustur,
    sifre_dogrula,
)
from app.crud.kullanici import (
    eposta_ile_kullanici_bul,
    kullanici_olustur,
)
from app.db.database import get_db
from app.models.departman import Departman
from app.models.kullanici import Kullanici
from app.schemas.auth import (
    GirisRequest,
    KayitRequest,
    TokenResponse,
)
from app.schemas.kullanici import (
    KullaniciCreate,
    KullaniciResponse,
)


router = APIRouter(tags=["Kimlik Doğrulama"])


# Yeni kullanıcıyı Personel rolüyle sisteme kaydeder
@router.post(
    "/kayit",
    response_model=KullaniciResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Yeni kullanıcı kaydı",
)
def kullanici_kaydi(
    kayit_bilgileri: KayitRequest,
    db: Session = Depends(get_db),
):
    temiz_eposta = str(
        kayit_bilgileri.eposta
    ).strip().lower()

    mevcut_kullanici = eposta_ile_kullanici_bul(
        db=db,
        eposta=temiz_eposta,
    )

    if mevcut_kullanici is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu e-posta adresi zaten kullanılıyor.",
        )

    departman = db.scalar(
        select(Departman).where(
            Departman.departman_id
            == kayit_bilgileri.departman_id
        )
    )

    if departman is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seçilen departman bulunamadı.",
        )

    kullanici_verisi = KullaniciCreate(
        ad_soyad=kayit_bilgileri.ad_soyad.strip(),
        eposta=temiz_eposta,
        sifre=kayit_bilgileri.sifre,
        rol="Personel",
        departman_id=kayit_bilgileri.departman_id,
        aktif_mi=True,
    )

    try:
        return kullanici_olustur(
            db=db,
            kullanici_verisi=kullanici_verisi,
        )
    except IntegrityError as error:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bu e-posta adresi zaten kullanılıyor.",
        ) from error


# E-posta ve parola ile giriş yaparak JWT token üretir
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
        eposta=str(
            giris_bilgileri.eposta
        ).strip().lower(),
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


# Geçerli token sahibi kullanıcının bilgilerini döndürür
@router.get(
    "/korumali-test",
    response_model=KullaniciResponse,
    summary="Token korumalı deneme endpoint'i",
)
def korumali_test(
    current_user: Kullanici = Depends(get_current_user),
):
    return current_user