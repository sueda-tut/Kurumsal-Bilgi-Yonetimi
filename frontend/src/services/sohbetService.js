// Sohbet oturumları ve RAG soru-cevap işlemlerini gerçekleştirir

import api from "../api/api";


// Kullanıcının sohbet oturumlarını getirir
export async function sohbetleriGetir() {
    const response = await api.get("/sohbetler");

    return response.data;
}


// Belirli bir sohbetin mesajlarını getirir
export async function sohbetMesajlariniGetir(oturumId) {
    const response = await api.get(
        `/sohbetler/${oturumId}`,
    );

    return response.data;
}


// Yeni veya mevcut oturum üzerinden AI'a soru gönderir
export async function soruSor({
    soru,
    oturumId = null,
    oturumBasligi = null,
}) {
    const istekVerisi = {
        soru,
    };

    if (oturumId) {
        istekVerisi.oturum_id = oturumId;
    } else if (oturumBasligi) {
        istekVerisi.oturum_basligi = oturumBasligi;
    }

    const response = await api.post(
        "/sor",
        istekVerisi,
    );

    return response.data;
}