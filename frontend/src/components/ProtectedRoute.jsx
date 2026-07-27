// Token bulunmayan kullanıcıların korumalı sayfalara erişmesini engeller

import { Navigate, Outlet } from "react-router-dom";


function ProtectedRoute() {
    const token = localStorage.getItem("access_token");

    if (!token) {
        return <Navigate to="/giris" replace />;
    }

    return <Outlet />;
}


export default ProtectedRoute;
