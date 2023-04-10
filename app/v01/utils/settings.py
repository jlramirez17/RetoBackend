"""
    Aplicación: Reto Backend Version v01
    Módulo: Llamada a los datos de conexión a la base de datos
    Fecha Creación: 06-04-2023
    Programador: José Luis Ramirez - JLRAMIREZ
    Descripción: LLamada al archivo .env que conitne los datos de la conexión a la BD PostgreSql
"""

import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

#OBTENEMOS LOS PARAMETROS DE CONEXIÓN A LA BD DESDE ARCHIVO .ENV

class Settings(BaseSettings):
    db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('5432')
    appname: str = os.getenv('APP_NAME')
    appcode: str = os.getenv('APP_CODE')
    version: str = os.getenv('APP_VERSION') 