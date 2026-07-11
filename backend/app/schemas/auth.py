from pydantic import BaseModel, EmailStr, Field


class GirisRequest(BaseModel):
    eposta: EmailStr
    sifre: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"