// Kullanıcı giriş ve kayıt isteklerini merkezi olarak yönetir

import api from "../api/api";


export async function girisYap({
    eposta,
    sifre,
}) {
    const response = await api.post("/giris", {
        eposta,
        sifre,
    });

    return response.data;
}


export async function kayitOl({
    adSoyad,
    eposta,
    sifre,
    sifreTekrar,
    departmanId,
}) {
    const response = await api.post("/kayit", {
        ad_soyad: adSoyad,
        eposta,
        sifre,
        sifre_tekrar: sifreTekrar,
        departman_id: departmanId,
    });

    return response.data;
}


export async function departmanlariGetir() {
    const response = await api.get("/departmanlar");

    return response.data;
}