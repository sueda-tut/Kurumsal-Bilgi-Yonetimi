from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Kullanici(Base):
    __tablename__ = "kullanicilar"

    kullanici_id = Column(Integer, primary_key=True, index=True)
    ad_soyad = Column(String(100), nullable=False)
    eposta = Column(String(150), nullable=False, unique=True, index=True)
    sifre_ozeti = Column(String(255), nullable=False)
    rol = Column(String(30), nullable=False)
    departman = Column(String(50), nullable=False)
    olusturulma_tarihi = Column(DateTime, nullable=False, server_default=func.now())

dokumanlar = relationship("Dokuman", back_populates="yukleyen_kullanici")

sohbet_oturumlari = relationship("SohbetOturumu", back_populates="kullanici")
