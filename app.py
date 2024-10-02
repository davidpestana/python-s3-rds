import os
import boto3
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Cargar variables de entorno
S3_BUCKET = os.getenv('S3_BUCKET')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
RDS_HOST = os.getenv('RDS_HOST')
RDS_PORT = os.getenv('RDS_PORT', 5432)
RDS_DB = os.getenv('RDS_DB')
RDS_USER = os.getenv('RDS_USER')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')

# Verificar conexión a S3
def check_s3_connection():
    try:
        print(f"verificar conexión a S3", flush=True)
        print(f"AWS_ACCESS_KEY: {AWS_ACCESS_KEY}", flush=True)
        print(f"AWS_SECRET_KEY: {AWS_SECRET_KEY}", flush=True)
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY
        )
        s3.list_buckets()  # Hacer una llamada simple para verificar la conexión
        print(f"Verificada conexión a S3", flush=True)
        return True
    except Exception as e:
        print(f"Error de conexión a S3: {e}")
        return False

# Verificar conexión a RDS
def check_rds_connection():
    try:
        print(f"verificar conexión a RDS", flush=True)

        connection = psycopg2.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            database=RDS_DB,
            user=RDS_USER,
            password=RDS_PASSWORD,
            ssl_disabled=True  # Deshabilitar SSL en MySQL
        )
        cursor = connection.cursor()
        cursor.execute("SELECT 1")  # Consulta simple para verificar la conexión
        cursor.close()
        connection.close()
        print(f"Verificada conexión a RDS", flush=True)
        return True
    except Exception as e:
        print(f"Error de conexión a RDS: {e}", flush=True)
        return False

# Endpoint para verificar el estado de las conexiones
@app.route('/status', methods=['GET'])
def status():
    s3_status = check_s3_connection()
    rds_status = check_rds_connection()

    return jsonify({
        's3_connection': 'successful' if s3_status else 'failed',
        'rds_connection': 'successful' if rds_status else 'failed'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
