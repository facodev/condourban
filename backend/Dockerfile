FROM python:3.14.5-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD ["poetry", "run", "fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
