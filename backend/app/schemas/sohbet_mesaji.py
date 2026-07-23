# Sohbet mesajlarına ait istek ve yanıt şemalarını tanımlar

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SohbetMesajiBase(BaseModel):
    mesaj_metni: str = Field(min_length=1)


class SohbetMesajiCreate(SohbetMesajiBase):
    oturum_id: int = Field(gt=0)
    gonderen_tipi: Literal["Kullanici", "AI"]


# Token sahibi kullanıcının mesaj gönderme isteğini tanımlar
class MesajGonderRequest(SohbetMesajiBase):
    pass


class SohbetMesajiResponse(SohbetMesajiBase):
    model_config = ConfigDict(from_attributes=True)

    mesaj_id: int
    oturum_id: int
    gonderen_tipi: str
    olusturulma_tarihi: datetime