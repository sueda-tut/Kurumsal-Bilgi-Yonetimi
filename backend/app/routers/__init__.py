# FastAPI router modüllerini tek noktadan dışa aktarır

from app.routers import (
    dokuman,
    etiket,
    kullanici,
    sohbet,
    yetki,
)


__all__ = [
    "dokuman",
    "etiket",
    "kullanici",
    "sohbet",
    "yetki",
]