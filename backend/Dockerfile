# Используем официальный образ Python на базе Alpine
FROM python:3.11-alpine

ENV UV_SYSTEM_PYTHON=1

# Обновляем pip и устанавливаем uv
RUN pip install --upgrade pip \
    && pip install uv

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы pyproject.toml и uv.lock
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости проекта
RUN uv sync --frozen --no-dev

# Копируем исходный код приложения
COPY . .

EXPOSE 8000

# Указываем команду для запуска приложения
CMD ["uv", "run", "-m", "app.main"]
