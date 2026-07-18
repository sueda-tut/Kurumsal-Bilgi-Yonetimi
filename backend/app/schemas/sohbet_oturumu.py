# Sohbet oturumlarının API giriş ve çıkış şemalarını tanımlar

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SohbetOturumuBase(BaseModel):
    kullanici_id: int = Field(gt=0)

    oturum_basligi: str = Field(
        min_length=1,
        max_length=200,
    )


class SohbetOturumuCreate(SohbetOturumuBase):
    pass


class SohbetOturumuResponse(SohbetOturumuBase):
    oturum_id: int
    baslangic_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)