from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DokumanBase(BaseModel):
    baslik: str = Field(min_length=2, max_length=200)
    departman: str = Field(min_length=2, max_length=50)


class DokumanCreate(DokumanBase):
    yukleyen_kullanici_id: int
    etiketler: list[str] = []
    yetkili_roller: list[str] = []


class DokumanUpdate(BaseModel):
    baslik: str | None = Field(default=None, min_length=2, max_length=200)
    departman: str | None = Field(default=None, min_length=2, max_length=50)
    surum_no: int | None = Field(default=None, ge=1)
    durum: str | None = Field(default=None, min_length=2, max_length=20)


class DokumanResponse(DokumanBase):
    dokuman_id: int
    dosya_adi: str
    dosya_turu: str
    yukleyen_kullanici_id: int
    yuklenme_tarihi: datetime
    surum_no: int
    dosya_yolu: str
    durum: str

    model_config = ConfigDict(from_attributes=True)


class DokumanDurumResponse(BaseModel):
    dokuman_id: int
    durum: str