# Usa una imagen base oficial de Python
FROM python:3.9-slim
# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app
# Copia el archivo de requerimientos y lo instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copia el código fuente en el directorio de trabajo
COPY . .
# Expone el puerto en el que se ejecutará la aplicación web
EXPOSE 5000
# Establece las variables de entorno para la app
ENV FLASK_ENV=production
# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
