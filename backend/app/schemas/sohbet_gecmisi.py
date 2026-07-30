# Geçmiş sohbet mesajlarını kaynaklarıyla birlikte döndüren şemaları tanımlar

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class GecmisMesajKaynagiResponse(BaseModel):
    kaynak_id: int
    dokuman_id: int
    dokuman_basligi: str
    parca_id: int
    parca_sirasi: int
    sayfa_no: int | None
    benzerlik_puani: Decimal

    model_config = ConfigDict(from_attributes=True)


class GecmisMesajResponse(BaseModel):
    mesaj_id: int
    oturum_id: int
    gonderen_tipi: str
    mesaj_metni: str
    olusturulma_tarihi: datetime
    kaynaklar: list[GecmisMesajKaynagiResponse] = Field(
        default_factory=list
    )

    model_config = ConfigDict(from_attributes=True)