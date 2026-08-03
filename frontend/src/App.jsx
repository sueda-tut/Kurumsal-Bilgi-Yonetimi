// Uygulamanın giriş ve korumalı sayfa yönlendirmelerini tanımlar

import {
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import AppLayout from "./components/AppLayout";
import ProtectedRoute from "./components/ProtectedRoute";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import DepartmentManagementPage from "./pages/DepartmentManagementPage";
import DocumentDetailPage from "./pages/DocumentDetailPage";
import DocumentsPage from "./pages/DocumentsPage";
import DocumentUploadPage from "./pages/DocumentUploadPage";
import LoginPage from "./pages/LoginPage";
import ProfilePage from "./pages/ProfilePage";
import RegisterPage from "./pages/RegisterPage";


function App() {
    return (
        <Routes>
            <Route
                path="/giris"
                element={<LoginPage />}
            />

            <Route
                path="/kayit"
                element={<RegisterPage />}
            />

            <Route element={<ProtectedRoute />}>
                <Route element={<AppLayout />}>
                    <Route
                        path="/panel"
                        element={<DashboardPage />}
                    />

                    <Route
                        path="/sohbet"
                        element={<ChatPage />}
                    />

                    <Route
                        path="/dokumanlar"
                        element={<DocumentsPage />}
                    />

                    <Route
                        path="/dokumanlar/yukle"
                        element={<DocumentUploadPage />}
                    />

                    <Route
                        path="/dokumanlar/:dokumanId"
                        element={<DocumentDetailPage />}
                    />

                    <Route
                        path="/departman-yonetimi"
                        element={<DepartmentManagementPage />}
                    />

                    <Route
                        path="/profil"
                        element={<ProfilePage />}
                    />
                </Route>
            </Route>

            <Route
                path="/"
                element={
                    <Navigate
                        to="/panel"
                        replace
                    />
                }
            />

            <Route
                path="*"
                element={
                    <Navigate
                        to="/panel"
                        replace
                    />
                }
            />
        </Routes>
    );
}


export default App;