from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Dokuman(Base):
    __tablename__ = "dokumanlar"

    dokuman_id = Column(Integer, primary_key=True, index=True)
    baslik = Column(String(200), nullable=False)
    dosya_adi = Column(String(255), nullable=False)
    dosya_turu = Column(String(10), nullable=False)
    yukleyen_kullanici_id = Column(
        Integer,
        ForeignKey("kullanicilar.kullanici_id"),
        nullable=False
    )
    yuklenme_tarihi = Column(DateTime, nullable=False, server_default=func.now())
    departman = Column(String(50), nullable=False)
    surum_no = Column(Integer, nullable=False, default=1)
    dosya_yolu = Column(String(300), nullable=False, unique=True)
    durum = Column(String(20), nullable=False)

    yukleyen_kullanici = relationship(
        "Kullanici",
        back_populates="dokumanlar"
    )

    parcalar = relationship(
        "DokumanParcasi",
        back_populates="dokuman",
        cascade="all, delete-orphan"
    )

    etiketler = relationship(
        "DokumanEtiketi",
        back_populates="dokuman",
        cascade="all, delete-orphan"
    )

    yetkiler = relationship(
        "DokumanYetkisi",
        back_populates="dokuman",
        cascade="all, delete-orphan"
    ) 