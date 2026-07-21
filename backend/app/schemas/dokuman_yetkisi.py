# Doküman departman yetkilerine ait istek ve yanıt şemalarını tanımlar

from pydantic import BaseModel, ConfigDict, Field


class DokumanYetkisiBase(BaseModel):
    departman_id: int = Field(gt=0)
    goruntuleyebilir_mi: bool = True


class DokumanYetkisiCreate(DokumanYetkisiBase):
    dokuman_id: int = Field(gt=0)


# Path üzerinden dokümana departman yetkisi ekleme isteğini tanımlar
class YetkiEkleRequest(DokumanYetkisiBase):
    pass


class DokumanYetkisiUpdate(BaseModel):
    goruntuleyebilir_mi: bool


class DokumanYetkisiResponse(DokumanYetkisiBase):
    model_config = ConfigDict(from_attributes=True)

    yetki_id: int
    dokuman_id: int