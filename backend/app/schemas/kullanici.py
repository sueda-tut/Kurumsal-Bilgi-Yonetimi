from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class KullaniciBase(BaseModel):
    ad_soyad: str = Field(min_length=2, max_length=100)
    eposta: EmailStr
    rol: str = Field(min_length=2, max_length=30)
    departman: str = Field(min_length=2, max_length=50)


class KullaniciCreate(KullaniciBase):
    sifre: str = Field(min_length=6, max_length=128)


class KullaniciUpdate(BaseModel):
    ad_soyad: str | None = Field(default=None, min_length=2, max_length=100)
    eposta: EmailStr | None = None
    sifre: str | None = Field(default=None, min_length=6, max_length=128)
    rol: str | None = Field(default=None, min_length=2, max_length=30)
    departman: str | None = Field(default=None, min_length=2, max_length=50)


class KullaniciResponse(KullaniciBase):
    kullanici_id: int
    olusturulma_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)