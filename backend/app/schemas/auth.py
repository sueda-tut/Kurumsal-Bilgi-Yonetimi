# Giriş işlemi ve JWT token yanıtı için şemaları tanımlar

from pydantic import BaseModel, EmailStr, Field


class GirisRequest(BaseModel):
    eposta: EmailStr
    sifre: str = Field(min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int