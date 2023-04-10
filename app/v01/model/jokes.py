"""
    Aplicación: Reto Backend Version v01
    Módulo: Modelo jokes chistes 
    Fecha Creación: 06-04-2023
    Programador: José Luis Ramirez - JLRAMIREZ
    Descripción: Definición del modelo jokes, tabla de la bd retobackend 
"""

from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Boolean, Integer, String
from app.v01.config.db import engine, Base

class Jokes(Base):
    __tablename__ = "jokes"

    id = Column(Integer, primary_key=True, autoincrement=True)    
    value = Column(String(5000), nullable=False)
    #create_at = Column(Date)

