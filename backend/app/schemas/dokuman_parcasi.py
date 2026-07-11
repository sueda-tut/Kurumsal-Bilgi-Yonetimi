from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DokumanParcasiCreate(BaseModel):
    dokuman_id: int
    parca_sirasi: int = Field(ge=1)
    parca_metni: str = Field(min_length=1)
    sayfa_no: int | None = Field(default=None, ge=1)
    token_sayisi: int = Field(gt=0)
    embedding_id: str | None = Field(default=None, max_length=100)


class DokumanParcasiResponse(BaseModel):
    parca_id: int
    dokuman_id: int
    parca_sirasi: int
    parca_metni: str
    sayfa_no: int | None
    token_sayisi: int
    embedding_id: str | None
    olusturulma_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)