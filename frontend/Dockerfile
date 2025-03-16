# Stage 1: Build stage
FROM node:18-alpine AS builder
WORKDIR /app
# Копируем файлы зависимостей
COPY package*.json ./
RUN npm install
# Копируем весь исходный код и собираем проект
COPY . .
RUN npm run build

# Stage 2: Production stage
FROM nginx:stable-alpine
# Копируем собранные файлы в папку, где Nginx выдаёт статику
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
