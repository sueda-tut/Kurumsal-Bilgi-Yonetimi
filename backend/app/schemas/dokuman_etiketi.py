# Doküman etiketlerine ait istek ve yanıt şemalarını tanımlar

from pydantic import BaseModel, ConfigDict, Field


class DokumanEtiketiBase(BaseModel):
    etiket_adi: str = Field(
        min_length=1,
        max_length=50,
    )


class DokumanEtiketiCreate(DokumanEtiketiBase):
    dokuman_id: int = Field(gt=0)


# Path üzerinden dokümana etiket ekleme isteğini tanımlar
class EtiketEkleRequest(DokumanEtiketiBase):
    pass


class DokumanEtiketiResponse(DokumanEtiketiBase):
    model_config = ConfigDict(from_attributes=True)

    dokuman_etiket_id: int
    dokuman_id: int