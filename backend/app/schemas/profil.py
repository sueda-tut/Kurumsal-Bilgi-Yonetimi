# Kullanıcının profil ekranında gösterilecek bilgileri tanımlar

from pydantic import BaseModel, ConfigDict, EmailStr


class ProfilResponse(BaseModel):
    kullanici_id: int
    ad_soyad: str
    eposta: EmailStr
    rol: str
    departman_id: int
    departman_adi: str
    aktif_mi: bool

    model_config = ConfigDict(from_attributes=True)