FROM python:3.11-slim

# Instala dependencias necesarias para Selenium + Chrome
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    fonts-liberation libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
    libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
    libxrandr2 libgbm1 libxshmfence1 libxss1 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y google-chrome-stable

# Crear carpeta app
WORKDIR /app

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar archivos de la app
COPY . .

# Exponer puerto para Flask
EXPOSE 8000

# Ejecutar la app Flask
CMD ["python", "app.py"]
