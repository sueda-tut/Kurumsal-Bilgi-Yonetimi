# Doküman parçalarının API giriş ve çıkış şemalarını tanımlar

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DokumanParcasiBase(BaseModel):
    dokuman_id: int = Field(gt=0)

    parca_sirasi: int = Field(ge=1)

    parca_metni: str = Field(min_length=1)

    sayfa_no: int | None = Field(
        default=None,
        ge=1,
    )

    token_sayisi: int = Field(gt=0)


class DokumanParcasiCreate(DokumanParcasiBase):
    pass


class DokumanParcasiResponse(DokumanParcasiBase):
    parca_id: int
    olusturulma_tarihi: datetime

    model_config = ConfigDict(from_attributes=True)