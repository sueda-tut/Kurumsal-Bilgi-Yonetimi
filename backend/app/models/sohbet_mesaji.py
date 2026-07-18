# Sohbet mesajları tablosunun SQLAlchemy modelini tanımlar

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class SohbetMesaji(Base):
    __tablename__ = "sohbet_mesajlari"

    __table_args__ = (
        CheckConstraint(
            "gonderen_tipi IN ('Kullanici', 'AI')",
            name="chk_sohbet_mesajlari_gonderen_tipi",
        ),
    )

    mesaj_id = Column(Integer, primary_key=True, index=True)

    oturum_id = Column(
        Integer,
        ForeignKey(
            "sohbet_oturumlari.oturum_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    gonderen_tipi = Column(
        String(20),
        nullable=False,
    )

    mesaj_metni = Column(
        Text,
        nullable=False,
    )

    olusturulma_tarihi = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    oturum = relationship(
        "SohbetOturumu",
        back_populates="mesajlar",
    )

    kaynaklar = relationship(
        "MesajKaynagi",
        back_populates="mesaj",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )