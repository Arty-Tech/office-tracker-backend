# Usa Python 3.11-slim (compatibile con asyncpg)
FROM python:3.11-slim

WORKDIR /app

# Installa gli strumenti di compilazione e le librerie PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
       libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt e installa le dipendenze Python
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia l’intera cartella app/ dentro /app
COPY app/ .

# Esponi la porta
EXPOSE 8000

# Imposta PYTHONPATH
ENV PYTHONPATH=/app

# Avvia l’applicazione con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]
