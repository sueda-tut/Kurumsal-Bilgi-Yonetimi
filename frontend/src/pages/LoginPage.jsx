// Kullanıcının FastAPI üzerinden giriş yapmasını sağlayan formu oluşturur

import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";

import api from "../api/api";


function LoginPage() {
    const navigate = useNavigate();

    const [eposta, setEposta] = useState("");
    const [sifre, setSifre] = useState("");
    const [hata, setHata] = useState("");
    const [yukleniyor, setYukleniyor] = useState(false);

    const mevcutToken = localStorage.getItem("access_token");

    if (mevcutToken) {
        return <Navigate to="/panel" replace />;
    }

    async function girisYap(event) {
        event.preventDefault();

        setHata("");
        setYukleniyor(true);

        try {
            const response = await api.post("/giris", {
                eposta: eposta.trim(),
                sifre,
            });

            localStorage.setItem(
                "access_token",
                response.data.access_token,
            );

            navigate("/panel", {
                replace: true,
            });
        } catch (error) {
            const hataMesaji =
                error.response?.data?.error?.message ||
                error.response?.data?.detail ||
                "Giriş yapılamadı. Bilgilerinizi kontrol edin.";

            setHata(hataMesaji);
        } finally {
            setYukleniyor(false);
        }
    }

    return (
        <main className="login-page">
            <section className="login-card">
                <div className="login-heading">
                    <span className="brand-badge">KB</span>

                    <div>
                        <h1>Kurumsal Bilgi Yönetimi</h1>
                        <p>Hesabınızla sisteme giriş yapın.</p>
                    </div>
                </div>

                <form onSubmit={girisYap}>
                    <label htmlFor="eposta">E-posta</label>

                    <input
                        id="eposta"
                        type="email"
                        value={eposta}
                        onChange={(event) =>
                            setEposta(event.target.value)
                        }
                        placeholder="ornek@kurumsal.com"
                        autoComplete="email"
                        required
                    />

                    <label htmlFor="sifre">Şifre</label>

                    <input
                        id="sifre"
                        type="password"
                        value={sifre}
                        onChange={(event) =>
                            setSifre(event.target.value)
                        }
                        placeholder="Şifrenizi girin"
                        autoComplete="current-password"
                        required
                    />

                    {hata && (
                        <p className="error-message">{hata}</p>
                    )}

                    <button
                        type="submit"
                        disabled={yukleniyor}
                    >
                        {yukleniyor
                            ? "Giriş yapılıyor..."
                            : "Giriş yap"}
                    </button>
                </form>
            </section>
        </main>
    );
}


export default LoginPage;
