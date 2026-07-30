// Korumalı sayfalarda ortak menü ve çıkış alanını oluşturur

import {
    NavLink,
    Outlet,
    useNavigate,
} from "react-router-dom";


function AppLayout() {
    const navigate = useNavigate();

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