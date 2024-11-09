# Usa una imagen base de Python
FROM python:3.9-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY ./requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta 'app' al contenedor
COPY . .

ENV PYTHONPATH=/app

# Establece el comando para ejecutar el consumidor
CMD ["python", "app/rabbit_consume/course_consume.py"]