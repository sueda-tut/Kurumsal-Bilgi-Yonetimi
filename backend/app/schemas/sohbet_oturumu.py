from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SohbetOturumuCreate(BaseModel):
    kullanici_id: int
    oturum_basligi: str = Field(min_length=1, max_length=200)


class SohbetOturumuResponse(BaseModel):
    oturum_id: int
    kullanici_id: int
    oturum_basligi: str
    baslangic_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)