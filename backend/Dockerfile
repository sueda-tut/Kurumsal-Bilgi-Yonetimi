# FastAPI backend uygulamasının Docker imajını oluşturur

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# psycopg2 ve bazı Python paketlerinin ihtiyaç duyduğu sistem araçlarını kurar
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıklarını önbellekten yararlanarak kurar
COPY backend/requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Backend ve AI modüllerini konteynere kopyalar
COPY backend/app ./app
COPY ai ./ai

# Yüklenen dosyaların tutulacağı klasörü oluşturur
RUN mkdir -p /app/uploads

EXPOSE 8000

# FastAPI uygulamasını başlatır
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]