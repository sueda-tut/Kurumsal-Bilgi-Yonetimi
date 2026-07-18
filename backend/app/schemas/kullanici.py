# Kullanıcı verilerinin güvenli API giriş ve çıkış şemalarını tanımlar

from datetime import datetime
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)


class KullaniciBase(BaseModel):
    ad_soyad: str = Field(
        min_length=2,
        max_length=100,
    )

    eposta: EmailStr

    rol: Literal[
        "Yonetici",
        "Personel",
    ]

    departman_id: int = Field(gt=0)

    aktif_mi: bool = True


class KullaniciCreate(KullaniciBase):
    sifre: str = Field(
        min_length=8,
        max_length=128,
    )


class KullaniciUpdate(BaseModel):
    ad_soyad: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    eposta: EmailStr | None = None

    sifre: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
    )

    rol: Literal[
        "Yonetici",
        "Personel",
    ] | None = None

    departman_id: int | None = Field(
        default=None,
        gt=0,
    )

    aktif_mi: bool | None = None


class KullaniciResponse(KullaniciBase):
    kullanici_id: int
    olusturulma_tarihi: datetime
    guncelleme_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)