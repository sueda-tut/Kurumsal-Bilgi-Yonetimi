// Doküman, departman ve etiket verilerini birleştiren API işlemlerini gerçekleştirir

import api from "../api/api";


// Departman listesini ID-ad eşlemesine dönüştürür
function departmanHaritasiOlustur(departmanlar) {
    return Object.fromEntries(
        departmanlar.map((departman) => [
            departman.departman_id,
            departman.departman_adi,
        ]),
    );
}


// Kullanıcının görebildiği dokümanları departman ve etiketleriyle getirir
export async function detayliDokumanlariGetir() {
    const [dokumanResponse, departmanResponse] =
        await Promise.all([
            api.get("/dokumanlar", {
                params: {
                    offset: 0,
                    limit: 100,
                },
            }),
            api.get("/departmanlar"),
        ]);

    const departmanHaritasi = departmanHaritasiOlustur(
        departmanResponse.data,
    );

    const detayliDokumanlar = await Promise.all(
        dokumanResponse.data.map(async (dokuman) => {
            const etiketResponse = await api.get(
                `/dokumanlar/${dokuman.dokuman_id}/etiketler`,
            );

            return {
                ...dokuman,
                departman_adi:
                    departmanHaritasi[dokuman.departman_id] ||
                    `Departman #${dokuman.departman_id}`,
                etiketler: etiketResponse.data.map(
                    (etiket) => etiket.etiket_adi,
                ),
            };
        }),
    );

    return detayliDokumanlar;
}


// Tek bir dokümanın detay, departman ve etiket bilgilerini getirir
export async function dokumanDetayiGetir(dokumanId) {
    const [
        dokumanResponse,
        departmanResponse,
        etiketResponse,
    ] = await Promise.all([
        api.get(`/dokumanlar/${dokumanId}`),
        api.get("/departmanlar"),
        api.get(`/dokumanlar/${dokumanId}/etiketler`),
    ]);

    const departmanHaritasi = departmanHaritasiOlustur(
        departmanResponse.data,
    );

    return {
        ...dokumanResponse.data,
        departman_adi:
            departmanHaritasi[
                dokumanResponse.data.departman_id
            ] ||
            `Departman #${dokumanResponse.data.departman_id}`,
        etiketler: etiketResponse.data.map(
            (etiket) => etiket.etiket_adi,
        ),
    };
}