// Uygulamanın giriş ve korumalı sayfa yönlendirmelerini tanımlar

import {
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";
import DashboardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";


function App() {
    return (
        <Routes>
            <Route
                path="/giris"
                element={<LoginPage />}
            />

            <Route element={<ProtectedRoute />}>
                <Route
                    path="/panel"
                    element={<DashboardPage />}
                />
            </Route>

            <Route
                path="/"
                element={<Navigate to="/panel" replace />}
            />

            <Route
                path="*"
                element={<Navigate to="/panel" replace />}
            />
        </Routes>
    );
}


export default App;