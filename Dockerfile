# backend/Dockerfile (versione con base python:3.13-slim)
FROM python:3.13-slim

# Impostiamo la working directory
WORKDIR /app

# Installiamo le dipendenze di sistema necessarie
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      gcc \
      libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamo il file requirements e installiamo le dipendenze Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiamo tutto il sorgente all'interno del container
COPY . .

# Esponiamo la porta (opzionale se usi docker-compose)
EXPOSE 8000

# Comando di avvio di default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
