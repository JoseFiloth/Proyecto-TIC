# Dockerfile
FROM python:3.10-slim

# Instalar dependencias necesarias
RUN apt update && apt install -y \
    build-essential gcc curl git stress-ng sysbench procps \
    && pip install --upgrade pip \
    && pip install psutil

# Crear directorio de trabajo
WORKDIR /app

# Copiar todos los archivos del proyecto al contenedor
COPY . .

# Exponer puertos si hicieras algo con Flask/Jupyter
EXPOSE 8888

CMD [ "bash" ]
