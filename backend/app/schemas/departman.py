# Departman verilerinin API giriş ve çıkış şemalarını tanımlar

from pydantic import BaseModel, ConfigDict, Field


class DepartmanBase(BaseModel):
    departman_adi: str = Field(
        min_length=2,
        max_length=50,
    )


class DepartmanCreate(DepartmanBase):
    pass


class DepartmanResponse(DepartmanBase):
    departman_id: int

    model_config = ConfigDict(from_attributes=True)