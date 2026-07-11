from pydantic import BaseModel, ConfigDict, Field


class DokumanYetkisiCreate(BaseModel):
    rol_adi: str = Field(min_length=1, max_length=30)
    goruntuleyebilir_mi: bool = True


class DokumanYetkisiUpdate(BaseModel):
    rol_adi: str | None = Field(default=None, min_length=1, max_length=30)
    goruntuleyebilir_mi: bool | None = None


class DokumanYetkisiResponse(BaseModel):
    yetki_id: int
    dokuman_id: int
    rol_adi: str
    goruntuleyebilir_mi: bool

    model_config = ConfigDict(from_attributes=True)