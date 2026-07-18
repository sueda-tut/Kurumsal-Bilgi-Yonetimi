# AI mesajlarının kullandığı doküman kaynaklarının API şemalarını tanımlar

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class MesajKaynagiBase(BaseModel):
    mesaj_id: int = Field(gt=0)

    parca_id: int = Field(gt=0)

    benzerlik_puani: Decimal = Field(
        ge=0,
        le=1,
        max_digits=5,
        decimal_places=4,
    )


class MesajKaynagiCreate(MesajKaynagiBase):
    pass


class MesajKaynagiResponse(MesajKaynagiBase):
    kaynak_id: int

    model_config = ConfigDict(from_attributes=True)