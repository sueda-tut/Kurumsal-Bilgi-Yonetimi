# Departman bazlı doküman yetkilerinin API şemalarını tanımlar

from pydantic import BaseModel, ConfigDict, Field


class DokumanYetkisiBase(BaseModel):
    dokuman_id: int = Field(gt=0)

    departman_id: int = Field(gt=0)

    goruntuleyebilir_mi: bool = True


class DokumanYetkisiCreate(DokumanYetkisiBase):
    pass


class DokumanYetkisiUpdate(BaseModel):
    goruntuleyebilir_mi: bool


class DokumanYetkisiResponse(DokumanYetkisiBase):
    yetki_id: int

    model_config = ConfigDict(from_attributes=True)