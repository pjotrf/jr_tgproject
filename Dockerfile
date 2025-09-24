FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Europe/Tallinn

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN useradd -m botuser && chown -R botuser:botuser /app
USER botuser

COPY healthcheck.py /app/healthcheck.py
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD ["python", "/app/healthcheck.py"]

CMD ["python", "bot.py"]
