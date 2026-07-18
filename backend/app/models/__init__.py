# SQLAlchemy modellerinin tamamını tek noktadan dışa aktarır

from app.models.departman import Departman
from app.models.dokuman import Dokuman
from app.models.dokuman_etiketi import DokumanEtiketi
from app.models.dokuman_parcasi import DokumanParcasi
from app.models.dokuman_yetkisi import DokumanYetkisi
from app.models.kullanici import Kullanici
from app.models.mesaj_kaynagi import MesajKaynagi
from app.models.sohbet_mesaji import SohbetMesaji
from app.models.sohbet_oturumu import SohbetOturumu


__all__ = [
    "Departman",
    "Dokuman",
    "DokumanEtiketi",
    "DokumanParcasi",
    "DokumanYetkisi",
    "Kullanici",
    "MesajKaynagi",
    "SohbetMesaji",
    "SohbetOturumu",
]