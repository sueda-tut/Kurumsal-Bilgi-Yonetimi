# Giriş, kullanıcı kaydı ve JWT token yanıtı şemalarını tanımlar

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    model_validator,
)


class GirisRequest(BaseModel):
    eposta: EmailStr
    sifre: str = Field(
        min_length=1,
        max_length=128,
    )


class KayitRequest(BaseModel):
    ad_soyad: str = Field(
        min_length=2,
        max_length=100,
    )

    eposta: EmailStr

    sifre: str = Field(
        min_length=8,
        max_length=72,
    )

    sifre_tekrar: str = Field(
        min_length=8,
        max_length=72,
    )

    departman_id: int = Field(gt=0)

    @model_validator(mode="after")
    def sifreleri_kontrol_et(self):
        if self.sifre != self.sifre_tekrar:
            raise ValueError("Şifreler birbiriyle aynı olmalıdır.")

        return self


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int