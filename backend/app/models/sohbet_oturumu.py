# Sohbet oturumları tablosunun SQLAlchemy modelini tanımlar

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class SohbetOturumu(Base):
    __tablename__ = "sohbet_oturumlari"

    oturum_id = Column(Integer, primary_key=True, index=True)

    kullanici_id = Column(
        Integer,
        ForeignKey("kullanicilar.kullanici_id"),
        nullable=False,
        index=True,
    )

    oturum_basligi = Column(
        String(200),
        nullable=False,
    )

    baslangic_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    kullanici = relationship(
        "Kullanici",
        back_populates="sohbet_oturumlari",
    )

    mesajlar = relationship(
        "SohbetMesaji",
        back_populates="oturum",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )