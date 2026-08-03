// Yeni personelin sisteme kayıt olmasını sağlayan formu oluşturur

import {
    useEffect,
    useState,
} from "react";
import {
    Link,
    Navigate,
    useNavigate,
} from "react-router-dom";

import {
    departmanlariGetir,
    kayitOl,
} from "../services/authService";


function hataMesajiGetir(error) {
    const detay = error.response?.data?.detail;

    if (Array.isArray(detay)) {
        return detay[0]?.msg || "Gönderilen bilgiler geçersiz.";
    }

    return (
        error.response?.data?.error?.message ||
        detay ||
        error.message ||
        "Kayıt işlemi gerçekleştirilemedi."
    );
}


function RegisterPage() {
    const navigate = useNavigate();

    const [adSoyad, setAdSoyad] = useState("");
    const [eposta, setEposta] = useState("");
    const [sifre, setSifre] = useState("");
    const [sifreTekrar, setSifreTekrar] = useState("");
    const [departmanId, setDepartmanId] = useState("");
    const [departmanlar, setDepartmanlar] = useState([]);
    const [hata, setHata] = useState("");
    const [yukleniyor, setYukleniyor] = useState(false);
    const [departmanlarYukleniyor, setDepartmanlarYukleniyor] =
        useState(true);

    const mevcutToken = localStorage.getItem("access_token");

    useEffect(() => {
        async function departmanlariYukle() {
            try {
                const sonuc = await departmanlariGetir();

                setDepartmanlar(sonuc);
            } catch (error) {
                setHata(hataMesajiGetir(error));
            } finally {
                setDepartmanlarYukleniyor(false);
            }
        }

        departmanlariYukle();
    }, []);

    if (mevcutToken) {
        return <Navigate to="/panel" replace />;
    }

    async function kayitFormunuGonder(event) {
        event.preventDefault();
        setHata("");

        if (sifre !== sifreTekrar) {
            setHata("Şifreler birbiriyle aynı olmalıdır.");
            return;
        }

        setYukleniyor(true);

        try {
            await kayitOl({
                adSoyad: adSoyad.trim(),
                eposta: eposta.trim().toLowerCase(),
                sifre,
                sifreTekrar,
                departmanId: Number(departmanId),
            });

            navigate("/giris", {
                replace: true,
                state: {
                    kayitBasarili:
                        "Kaydınız oluşturuldu. Şimdi giriş yapabilirsiniz.",
                },
            });
        } catch (error) {
            setHata(hataMesajiGetir(error));
        } finally {
            setYukleniyor(false);
        }
    }

    return (
        <main className="login-page">
            <section className="login-card register-card">
                <div className="login-heading">
                    <span className="brand-badge">KB</span>

                    <div>
                        <h1>Kullanıcı Kaydı</h1>
                        <p>
                            Personel hesabınızı oluşturarak
                            sisteme katılın.
                        </p>
                    </div>
                </div>

                <form onSubmit={kayitFormunuGonder}>
                    <label htmlFor="ad-soyad">
                        Ad soyad
                    </label>

                    <input
                        id="ad-soyad"
                        type="text"
                        value={adSoyad}
                        onChange={(event) =>
                            setAdSoyad(event.target.value)
                        }
                        placeholder="Adınız ve soyadınız"
                        autoComplete="name"
                        minLength={2}
                        maxLength={100}
                        required
                    />

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

                    <label htmlFor="departman">
                        Departman
                    </label>

                    <select
                        id="departman"
                        value={departmanId}
                        onChange={(event) =>
                            setDepartmanId(event.target.value)
                        }
                        disabled={departmanlarYukleniyor}
                        required
                    >
                        <option value="">
                            {departmanlarYukleniyor
                                ? "Departmanlar yükleniyor..."
                                : "Departman seçin"}
                        </option>

                        {departmanlar.map((departman) => (
                            <option
                                key={departman.departman_id}
                                value={departman.departman_id}
                            >
                                {departman.departman_adi}
                            </option>
                        ))}
                    </select>

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
                        placeholder="En az 8 karakter"
                        autoComplete="new-password"
                        minLength={8}
                        maxLength={72}
                        required
                    />

                    <label htmlFor="sifre-tekrar">
                        Şifre tekrarı
                    </label>

                    <input
                        id="sifre-tekrar"
                        type="password"
                        value={sifreTekrar}
                        onChange={(event) =>
                            setSifreTekrar(event.target.value)
                        }
                        placeholder="Şifrenizi tekrar girin"
                        autoComplete="new-password"
                        minLength={8}
                        maxLength={72}
                        required
                    />

                    {hata && (
                        <p className="error-message">
                            {hata}
                        </p>
                    )}

                    <button
                        type="submit"
                        disabled={
                            yukleniyor ||
                            departmanlarYukleniyor
                        }
                    >
                        {yukleniyor
                            ? "Kayıt oluşturuluyor..."
                            : "Kayıt ol"}
                    </button>
                </form>

                <p className="auth-switch-text">
                    Zaten hesabınız var mı?{" "}
                    <Link to="/giris">
                        Giriş yapın
                    </Link>
                </p>
            </section>
        </main>
    );
}


export default RegisterPage;