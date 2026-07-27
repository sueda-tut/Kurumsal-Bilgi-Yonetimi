// Korumalı sayfalarda ortak menü, başlık ve çıkış alanını oluşturur

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
                        className={({ isActive }) =>
                            isActive ? "nav-link active" : "nav-link"
                        }
                    >
                        Dashboard
                    </NavLink>

                    <NavLink
                        to="/dokumanlar"
                        className={({ isActive }) =>
                            isActive ? "nav-link active" : "nav-link"
                        }
                    >
                        Dokümanlar
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