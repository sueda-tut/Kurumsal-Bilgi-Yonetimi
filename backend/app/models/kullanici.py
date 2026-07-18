# Kullanıcılar tablosunun SQLAlchemy modelini tanımlar

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Kullanici(Base):
    __tablename__ = "kullanicilar"

    __table_args__ = (
        CheckConstraint(
            "rol IN ('Yonetici', 'Personel')",
            name="chk_kullanicilar_rol",
        ),
    )

    kullanici_id = Column(Integer, primary_key=True, index=True)

    ad_soyad = Column(
        String(100),
        nullable=False,
    )

    eposta = Column(
        String(150),
        nullable=False,
        unique=True,
    )

    sifre_ozeti = Column(
        String(255),
        nullable=False,
    )

    rol = Column(
        String(30),
        nullable=False,
    )

    departman_id = Column(
        Integer,
        ForeignKey("departmanlar.departman_id"),
        nullable=False,
        index=True,
    )

    aktif_mi = Column(
        Boolean,
        nullable=False,
        server_default=text("TRUE"),
    )

    olusturulma_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    guncelleme_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    departman = relationship(
        "Departman",
        back_populates="kullanicilar",
    )

    dokumanlar = relationship(
        "Dokuman",
        back_populates="yukleyen_kullanici",
        foreign_keys="Dokuman.yukleyen_kullanici_id",
    )

    sohbet_oturumlari = relationship(
        "SohbetOturumu",
        back_populates="kullanici",
    )