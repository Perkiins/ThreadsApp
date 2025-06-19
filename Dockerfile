FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para Playwright y navegador
RUN apt-get update && apt-get install -y \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libpango1.0-0 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libnss3 \
    libxss1 \
    libgtk-3-0 \
    libxshmfence1 \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Crear carpeta para la app
WORKDIR /app

# Copiar requirements.txt y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install

# Copiar el código de la app
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
