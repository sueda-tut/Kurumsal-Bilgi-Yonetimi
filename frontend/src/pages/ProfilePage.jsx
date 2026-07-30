// Giriş yapan kullanıcının profil bilgilerini gösterir

import { useEffect, useState } from "react";

import { profilGetir } from "../services/profilService";


function hataMesajiGetir(error) {
    return (
        error.response?.data?.error?.message ||
        error.response?.data?.detail ||
        error.message ||
        "Profil bilgileri alınamadı."
    );
}


function ProfilePage() {
    const [profil, setProfil] = useState(null);
    const [yukleniyor, setYukleniyor] = useState(true);
    const [hata, setHata] = useState("");

    useEffect(() => {
        async function profiliYukle() {
            try {
                const sonuc = await profilGetir();

                setProfil(sonuc);
            } catch (error) {
                setHata(hataMesajiGetir(error));
            } finally {
                setYukleniyor(false);
            }
        }

        profiliYukle();
    }, []);

    if (yukleniyor) {
        return (
            <main className="profile-page">
                <div className="profile-state-card">
                    <span className="loading-spinner" />
                    <p>Profil bilgileri yükleniyor...</p>
                </div>
            </main>
        );
    }

    if (hata) {
        return (
            <main className="profile-page">
                <div className="profile-state-card profile-error">
                    <h1>Profil yüklenemedi</h1>
                    <p>{hata}</p>
                </div>
            </main>
        );
    }

    return (
        <main className="profile-page">
            <section className="profile-header">
                <div>
                    <p className="eyebrow">Kullanıcı hesabı</p>
                    <h1>Profilim</h1>
                    <p>
                        Kurumsal Bilgi Yönetimi hesabınıza ait
                        bilgiler.
                    </p>
                </div>

                <span
                    className={
                        profil.aktif_mi
                            ? "profile-status active"
                            : "profile-status passive"
                    }
                >
                    {profil.aktif_mi ? "Aktif hesap" : "Pasif hesap"}
                </span>
            </section>

            <section className="profile-card">
                <div className="profile-identity">
                    <div className="profile-avatar">
                        {profil.ad_soyad
                            ?.trim()
                            .charAt(0)
                            .toLocaleUpperCase("tr-TR")}
                    </div>

                    <div>
                        <h2>{profil.ad_soyad}</h2>
                        <p>{profil.eposta}</p>
                    </div>
                </div>

                <div className="profile-information-grid">
                    <article className="profile-information-item">
                        <span>Ad soyad</span>
                        <strong>{profil.ad_soyad}</strong>
                    </article>

                    <article className="profile-information-item">
                        <span>E-posta</span>
                        <strong>{profil.eposta}</strong>
                    </article>

                    <article className="profile-information-item">
                        <span>Rol</span>
                        <strong>{profil.rol}</strong>
                    </article>

                    <article className="profile-information-item">
                        <span>Departman</span>
                        <strong>{profil.departman_adi}</strong>
                    </article>

                    <article className="profile-information-item">
                        <span>Kullanıcı numarası</span>
                        <strong>#{profil.kullanici_id}</strong>
                    </article>

                    <article className="profile-information-item">
                        <span>Departman numarası</span>
                        <strong>#{profil.departman_id}</strong>
                    </article>
                </div>
            </section>
        </main>
    );
}


export default ProfilePage;