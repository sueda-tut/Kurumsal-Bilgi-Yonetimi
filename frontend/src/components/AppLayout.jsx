// Korumalı sayfalarda ortak menü, yönetici bağlantısı ve çıkış alanını oluşturur

import {
    useEffect,
    useState,
} from "react";
import {
    NavLink,
    Outlet,
    useNavigate,
} from "react-router-dom";

import { profilGetir } from "../services/profilService";


function AppLayout() {
    const navigate = useNavigate();
    const [yoneticiMi, setYoneticiMi] = useState(false);

    useEffect(() => {
        let aktif = true;

        async function kullaniciRolunuGetir() {
            try {
                const profil = await profilGetir();

                if (aktif) {
                    setYoneticiMi(
                        profil.rol === "Yonetici",
                    );
                }
            } catch {
                if (aktif) {
                    setYoneticiMi(false);
                }
            }
        }

        kullaniciRolunuGetir();

        return () => {
            aktif = false;
        };
    }, []);

    function cikisYap() {
        localStorage.removeItem("access_token");

        navigate("/giris", {
            replace: true,
        });
    }

    function navSinifi({ isActive }) {
        return isActive
            ? "nav-link active"
            : "nav-link";
    }

    return (
        <div className="app-shell">
            <header className="app-header">
                <NavLink
                    to="/panel"
                    className="app-brand"
                >
                    <span className="brand-badge">KB</span>
                    <span>Kurumsal Bilgi Yönetimi</span>
                </NavLink>

                <nav className="app-navigation">
                    <NavLink
                        to="/panel"
                        className={navSinifi}
                    >
                        Dashboard
                    </NavLink>

                    <NavLink
                        to="/sohbet"
                        className={navSinifi}
                    >
                        AI Sohbet
                    </NavLink>

                    <NavLink
                        to="/dokumanlar"
                        end
                        className={navSinifi}
                    >
                        Dokümanlar
                    </NavLink>

                    <NavLink
                        to="/dokumanlar/yukle"
                        className={navSinifi}
                    >
                        Doküman Yükle
                    </NavLink>

                    {yoneticiMi && (
                        <NavLink
                            to="/departman-yonetimi"
                            className={navSinifi}
                        >
                            Departmanlar
                        </NavLink>
                    )}

                    <NavLink
                        to="/profil"
                        className={navSinifi}
                    >
                        Profil
                    </NavLink>
                </nav>

                <button
                    type="button"
                    className="logout-button"
                    onClick={cikisYap}
                >
                    Çıkış yap
                </button>
            </header>

            <Outlet />
        </div>
    );
}


export default AppLayout;