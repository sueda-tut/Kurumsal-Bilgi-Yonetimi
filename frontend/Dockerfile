# React uygulamasını derler ve Nginx üzerinden sunar

FROM node:22-alpine AS build

WORKDIR /app

# Bağımlılık dosyalarını önce kopyalayarak Docker önbelleğini kullanır
COPY frontend/package.json frontend/package-lock.json ./

RUN npm ci

# Frontend kaynak kodunu kopyalar
COPY frontend/ ./

ARG VITE_API_URL=http://127.0.0.1:8000
ENV VITE_API_URL=${VITE_API_URL}

# React uygulamasının üretim sürümünü oluşturur
RUN npm run build


# Oluşturulan statik dosyaları Nginx üzerinden sunar
FROM nginx:1.27-alpine

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]