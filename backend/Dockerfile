FROM python:3.9-slim

# Instalación de dependencias del sistema (como curl)
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpq-dev

# Instalar Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

# Asegúrate de que Cargo esté en el PATH
ENV PATH="/root/.cargo/bin:${PATH}"

ENV YOUTUBE_API_KEY=tu_api_key_aqui


# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m nltk.downloader stopwords


# Copiar el resto de la aplicación
COPY . /app
WORKDIR /app

# Expón el puerto 8080
EXPOSE 8080

CMD ["python", "app.py"]
