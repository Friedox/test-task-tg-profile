FROM python:3.11-alpine

ENV UV_SYSTEM_PYTHON=1

RUN pip install --upgrade pip \
    && pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "-m", "app.main"]
