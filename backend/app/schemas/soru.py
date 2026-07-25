# Soru sorma endpoint'inin istek, cevap ve kaynak şemalarını tanımlar

from pydantic import BaseModel, Field


class SoruRequest(BaseModel):
    soru: str = Field(
        min_length=1,
        max_length=4000,
    )

    oturum_id: int | None = Field(
        default=None,
        gt=0,
    )

    oturum_basligi: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )


class SoruKaynagiResponse(BaseModel):
    kaynak_id: int
    dokuman_id: int
    dokuman_basligi: str
    parca_id: int
    parca_sirasi: int
    sayfa_no: int | None
    benzerlik_puani: float


class SoruResponse(BaseModel):
    oturum_id: int
    kullanici_mesaj_id: int
    ai_mesaj_id: int
    cevap: str
    kaynaklar: list[SoruKaynagiResponse]