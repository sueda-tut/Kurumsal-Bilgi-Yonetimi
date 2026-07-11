from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class SohbetOturumu(Base):
    __tablename__ = "sohbet_oturumlari"

    oturum_id = Column(Integer, primary_key=True, index=True)
    kullanici_id = Column(
        Integer,
        ForeignKey("kullanicilar.kullanici_id"),
        nullable=False
    )
    oturum_basligi = Column(String(200), nullable=False)
    baslangic_tarihi = Column(DateTime, nullable=False, server_default=func.now())

    kullanici = relationship(
        "Kullanici",
        back_populates="sohbet_oturumlari"
    )

    mesajlar = relationship(
        "SohbetMesaji",
        back_populates="oturum",
        cascade="all, delete-orphan"
    )