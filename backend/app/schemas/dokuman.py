# Doküman verilerinin API giriş, güncelleme ve çıkış şemalarını tanımlar

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


DosyaTuru = Literal[
    "pdf",
    "docs",
    "xlsx",
]

DokumanDurumu = Literal[
    "Isleniyor",
    "Aktif",
    "Hata",
    "Arsiv",
]


class DokumanBase(BaseModel):
    baslik: str = Field(
        min_length=1,
        max_length=200,
    )

    dosya_adi: str = Field(
        min_length=1,
        max_length=255,
    )

    dosya_turu: DosyaTuru

    yukleyen_kullanici_id: int = Field(gt=0)

    departman_id: int = Field(gt=0)

    surum_no: int = Field(
        default=1,
        ge=1,
    )

    dosya_yolu: str = Field(
        min_length=1,
        max_length=300,
    )

    durum: DokumanDurumu = "Isleniyor"

    dosya_boyutu: int = Field(gt=0)


class DokumanCreate(DokumanBase):
    pass


class DokumanUpdate(BaseModel):
    baslik: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    dosya_adi: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    dosya_turu: DosyaTuru | None = None

    yukleyen_kullanici_id: int | None = Field(
        default=None,
        gt=0,
    )

    departman_id: int | None = Field(
        default=None,
        gt=0,
    )

    surum_no: int | None = Field(
        default=None,
        ge=1,
    )

    dosya_yolu: str | None = Field(
        default=None,
        min_length=1,
        max_length=300,
    )

    durum: DokumanDurumu | None = None

    dosya_boyutu: int | None = Field(
        default=None,
        gt=0,
    )


class DokumanResponse(DokumanBase):
    dokuman_id: int
    yuklenme_tarihi: datetime
    guncelleme_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)


class DokumanDurumResponse(BaseModel):
    dokuman_id: int
    durum: DokumanDurumu
    guncelleme_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)