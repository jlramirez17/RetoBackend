"""
    Aplicación: Reto Backend Version v01
    Módulo: Configuración de conexión a la base de datos
    Fecha Creación: 06-04-2023
    Programador: José Luis Ramirez - JLRAMIREZ
    Descripción: Definición de la configuración de la conexión a la BD PostgreSql
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.v01.utils.settings import Settings

settings = Settings()

DB_NAME = settings.db_name
DB_USER = settings.db_user
DB_PASS = settings.db_pass
DB_HOST = settings.db_host
DB_PORT = settings.db_port

DATABASE_URL = "postgresql://"+DB_USER+":"+DB_PASS+"@"+DB_HOST+":"+DB_PORT+"/"+DB_NAME

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()




