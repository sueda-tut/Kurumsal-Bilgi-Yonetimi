// Kullanıcının FastAPI üzerinden giriş yapmasını sağlayan formu oluşturur

import { useState } from "react";
import {
    Link,
    Navigate,
    useLocation,
    useNavigate,
} from "react-router-dom";

import { girisYap } from "../services/authService";


function LoginPage() {
    const navigate = useNavigate();
    const location = useLocation();

    const [eposta, setEposta] = useState("");
    const [sifre, setSifre] = useState("");
    const [hata, setHata] = useState("");
    const [yukleniyor, setYukleniyor] = useState(false);

    const mevcutToken = localStorage.getItem("access_token");
    const basariMesaji = location.state?.kayitBasarili;

    if (mevcutToken) {
        return <Navigate to="/panel" replace />;
    }

    async function girisFormunuGonder(event) {
        event.preventDefault();

        setHata("");
        setYukleniyor(true);

        try {
            const sonuc = await girisYap({
                eposta: eposta.trim().toLowerCase(),
                sifre,
            });

            localStorage.setItem(
                "access_token",
                sonuc.access_token,
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
                        <p>
                            Hesabınızla sisteme giriş yapın.
                        </p>
                    </div>
                </div>

                {basariMesaji && (
                    <p className="success-message">
                        {basariMesaji}
                    </p>
                )}

                <form onSubmit={girisFormunuGonder}>
                    <label htmlFor="eposta">
                        E-posta
                    </label>

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

                    <label htmlFor="sifre">
                        Şifre
                    </label>

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
                        <p className="error-message">
                            {hata}
                        </p>
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

                <p className="auth-switch-text">
                    Henüz hesabınız yok mu?{" "}
                    <Link to="/kayit">
                        Kayıt olun
                    </Link>
                </p>
            </section>
        </main>
    );
}


export default LoginPage;