# Sohbet oturumlarına ait istek ve yanıt şemalarını tanımlar

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SohbetOturumuBase(BaseModel):
    oturum_basligi: str = Field(
        min_length=1,
        max_length=255,
    )


class SohbetOturumuCreate(SohbetOturumuBase):
    kullanici_id: int = Field(gt=0)


# Token sahibi kullanıcı için yeni sohbet isteğini tanımlar
class SohbetOlusturRequest(SohbetOturumuBase):
    pass


class SohbetOturumuResponse(SohbetOturumuBase):
    model_config = ConfigDict(from_attributes=True)

    oturum_id: int
    kullanici_id: int
    baslangic_tarihi: datetime