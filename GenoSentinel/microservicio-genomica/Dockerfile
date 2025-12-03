# Imagen base ligera de Python
FROM python:3.11-slim

# Evitar buffer en logs y crear directorio de la app
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Instalar dependencias del sistema para compilar algunas libs (MySQL, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalarlos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto donde corre Django
EXPOSE 8000

# Comando por defecto: correr la aplicación con gunicorn (más apropiado para Kubernetes)
CMD ["gunicorn", "genomic_service.wsgi:application", "--bind", "0.0.0.0:8000"]