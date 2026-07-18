# Doküman etiketlerinin API giriş ve çıkış şemalarını tanımlar

from pydantic import BaseModel, ConfigDict, Field


class DokumanEtiketiBase(BaseModel):
    dokuman_id: int = Field(gt=0)

    etiket_adi: str = Field(
        min_length=1,
        max_length=50,
    )


class DokumanEtiketiCreate(DokumanEtiketiBase):
    pass


class DokumanEtiketiResponse(DokumanEtiketiBase):
    dokuman_etiket_id: int

    model_config = ConfigDict(from_attributes=True)