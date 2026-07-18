# Sohbet mesajlarının API giriş ve çıkış şemalarını tanımlar

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


GonderenTipi = Literal[
    "Kullanici",
    "AI",
]


class SohbetMesajiBase(BaseModel):
    oturum_id: int = Field(gt=0)

    gonderen_tipi: GonderenTipi

    mesaj_metni: str = Field(min_length=1)


class SohbetMesajiCreate(SohbetMesajiBase):
    pass


class SohbetMesajiResponse(SohbetMesajiBase):
    mesaj_id: int
    olusturulma_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)