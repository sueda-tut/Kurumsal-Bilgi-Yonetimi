-- Dokümanın Chunk Sayısını Döndüren Function

CREATE OR REPLACE FUNCTION fn_chunk_sayisi(
    p_dokuman_id INTEGER
)

RETURNS INTEGER

LANGUAGE plpgsql

AS
$$
BEGIN

    RETURN
    (
        SELECT COUNT(*)
        FROM dokuman_parcalari
        WHERE dokuman_id = p_dokuman_id
    );

END;
$$;

-- Dokümanın Toplam Token Sayısını Döndüren Function

CREATE OR REPLACE FUNCTION fn_token_sayisi(
    p_dokuman_id INTEGER
)

RETURNS INTEGER

LANGUAGE plpgsql

AS
$$
BEGIN

    RETURN
    (
        SELECT COALESCE(SUM(token_sayisi),0)
        FROM dokuman_parcalari
        WHERE dokuman_id = p_dokuman_id
    );

END;
$$;

-- Kullanıcının Yüklediği Doküman Sayısını Döndüren Function

CREATE OR REPLACE FUNCTION fn_kullanici_dokuman_sayisi(
    p_kullanici_id INTEGER
)

RETURNS INTEGER

LANGUAGE plpgsql

AS
$$
BEGIN

    RETURN
    (
        SELECT COUNT(*)
        FROM dokumanlar
        WHERE yukleyen_kullanici_id = p_kullanici_id
    );

END;
$$;

-- Sohbetteki Mesaj Sayısını Döndüren Function

CREATE OR REPLACE FUNCTION fn_sohbet_mesaj_sayisi(
    p_oturum_id INTEGER
)

RETURNS INTEGER

LANGUAGE plpgsql

AS
$$
BEGIN

    RETURN
    (
        SELECT COUNT(*)
        FROM sohbet_mesajlari
        WHERE oturum_id = p_oturum_id
    );

END;
$$;

-- Dokümanın Etiket Sayısını Döndüren Function

CREATE OR REPLACE FUNCTION fn_dokuman_etiket_sayisi(
    p_dokuman_id INTEGER
)

RETURNS INTEGER

LANGUAGE plpgsql

AS
$$
BEGIN

    RETURN
    (
        SELECT COUNT(*)
        FROM dokuman_etiketleri
        WHERE dokuman_id = p_dokuman_id
    );

END;
$$;