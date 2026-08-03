// Yöneticinin departmanları görüntülemesini ve yeni departman eklemesini sağlar

import {
    useEffect,
    useState,
} from "react";

import {
    departmanOlustur,
    departmanlariGetir,
} from "../services/departmanService";
import { profilGetir } from "../services/profilService";


function hataMesajiGetir(error) {
    const hataVerisi = error.response?.data;

    if (Array.isArray(hataVerisi?.detail)) {
        return hataVerisi.detail
            .map((hata) => hata.msg)
            .join(", ");
    }

    return (
        hataVerisi?.error?.message ||
        hataVerisi?.detail ||
        error.message ||
        "İşlem gerçekleştirilemedi."
    );
}


function DepartmentManagementPage() {
    const [profil, setProfil] = useState(null);
    const [departmanlar, setDepartmanlar] = useState([]);
    const [departmanAdi, setDepartmanAdi] = useState("");
    const [yukleniyor, setYukleniyor] = useState(true);
    const [kaydediliyor, setKaydediliyor] = useState(false);
    const [hata, setHata] = useState("");
    const [basariMesaji, setBasariMesaji] = useState("");

    useEffect(() => {
        async function sayfayiYukle() {
            try {
                const [profilSonucu, departmanSonucu] =
                    await Promise.all([
                        profilGetir(),
                        departmanlariGetir(),
                    ]);

                setProfil(profilSonucu);
                setDepartmanlar(departmanSonucu);
            } catch (error) {
                setHata(hataMesajiGetir(error));
            } finally {
                setYukleniyor(false);
            }
        }

        sayfayiYukle();
    }, []);

    async function formuGonder(event) {
        event.preventDefault();

        const temizDepartmanAdi =
            departmanAdi.trim();

        if (temizDepartmanAdi.length < 2) {
            setHata(
                "Departman adı en az 2 karakter olmalıdır.",
            );
            setBasariMesaji("");

            return;
        }

        setKaydediliyor(true);
        setHata("");
        setBasariMesaji("");

        try {
            const yeniDepartman =
                await departmanOlustur(
                    temizDepartmanAdi,
                );

            setDepartmanlar((mevcutDepartmanlar) => [
                ...mevcutDepartmanlar,
                yeniDepartman,
            ]);

            setDepartmanAdi("");
            setBasariMesaji(
                `${yeniDepartman.departman_adi} departmanı başarıyla eklendi.`,
            );
        } catch (error) {
            setHata(hataMesajiGetir(error));
        } finally {
            setKaydediliyor(false);
        }
    }

    if (yukleniyor) {
        return (
            <main className="department-page">
                <section className="department-state-card">
                    <span className="loading-spinner" />
                    <p>Departman bilgileri yükleniyor...</p>
                </section>
            </main>
        );
    }

    if (hata && !profil) {
        return (
            <main className="department-page">
                <section className="department-state-card">
                    <h1>Sayfa yüklenemedi</h1>
                    <p className="error-message">{hata}</p>
                </section>
            </main>
        );
    }

    if (profil?.rol !== "Yonetici") {
        return (
            <main className="department-page">
                <section className="department-state-card access-denied">
                    <span className="access-denied-icon">!</span>

                    <div>
                        <p className="eyebrow">Yetkisiz erişim</p>
                        <h1>Bu sayfaya erişemezsiniz</h1>
                        <p>
                            Departman yönetimi yalnızca yönetici
                            hesapları tarafından kullanılabilir.
                        </p>
                    </div>
                </section>
            </main>
        );
    }

    return (
        <main className="department-page">
            <section className="department-page-header">
                <div>
                    <p className="eyebrow">Yönetici işlemleri</p>
                    <h1>Departman Yönetimi</h1>
                    <p>
                        Sistemdeki departmanları görüntüleyebilir
                        ve yeni departman oluşturabilirsiniz.
                    </p>
                </div>

                <div className="department-count-card">
                    <strong>{departmanlar.length}</strong>
                    <span>Toplam departman</span>
                </div>
            </section>

            <div className="department-content-grid">
                <section className="department-list-card">
                    <div className="department-card-heading">
                        <div>
                            <p className="eyebrow">Kayıtlı birimler</p>
                            <h2>Departmanlar</h2>
                        </div>
                    </div>

                    <div className="department-list">
                        {departmanlar.map((departman) => (
                            <article
                                key={departman.departman_id}
                                className="department-list-item"
                            >
                                <span className="department-icon">
                                    {departman.departman_adi
                                        .charAt(0)
                                        .toLocaleUpperCase("tr-TR")}
                                </span>

                                <div>
                                    <strong>
                                        {departman.departman_adi}
                                    </strong>

                                    <span>
                                        Departman #
                                        {departman.departman_id}
                                    </span>
                                </div>
                            </article>
                        ))}
                    </div>
                </section>

                <section className="department-form-card">
                    <p className="eyebrow">Yeni kayıt</p>
                    <h2>Departman ekle</h2>
                    <p>
                        Sisteme eklenecek departmanın adını girin.
                    </p>

                    <form
                        className="department-form"
                        onSubmit={formuGonder}
                    >
                        <label htmlFor="departman-adi">
                            Departman adı
                        </label>

                        <input
                            id="departman-adi"
                            type="text"
                            value={departmanAdi}
                            minLength={2}
                            maxLength={50}
                            placeholder="Örneğin: Ar-Ge"
                            disabled={kaydediliyor}
                            onChange={(event) => {
                                setDepartmanAdi(
                                    event.target.value,
                                );
                                setHata("");
                                setBasariMesaji("");
                            }}
                        />

                        {hata && (
                            <p className="error-message">
                                {hata}
                            </p>
                        )}

                        {basariMesaji && (
                            <p className="success-message">
                                {basariMesaji}
                            </p>
                        )}

                        <button
                            type="submit"
                            className="primary-button"
                            disabled={
                                kaydediliyor ||
                                departmanAdi.trim().length < 2
                            }
                        >
                            {kaydediliyor
                                ? "Departman ekleniyor..."
                                : "Departmanı ekle"}
                        </button>
                    </form>
                </section>
            </div>
        </main>
    );
}


export default DepartmentManagementPage;