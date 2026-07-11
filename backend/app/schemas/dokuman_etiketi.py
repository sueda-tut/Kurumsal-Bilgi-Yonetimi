from pydantic import BaseModel, ConfigDict, Field


class DokumanEtiketiCreate(BaseModel):
    etiket_adi: str = Field(min_length=1, max_length=50)


class DokumanEtiketiResponse(BaseModel):
    dokuman_etiket_id: int
    dokuman_id: int
    etiket_adi: str

    model_config = ConfigDict(from_attributes=True)