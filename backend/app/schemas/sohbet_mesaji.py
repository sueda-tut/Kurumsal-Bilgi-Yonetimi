from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SohbetMesajiCreate(BaseModel):
    oturum_id: int
    mesaj_metni: str = Field(min_length=1)


class SohbetMesajiResponse(BaseModel):
    mesaj_id: int
    oturum_id: int
    gonderen_tipi: str
    mesaj_metni: str
    olusturulma_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)