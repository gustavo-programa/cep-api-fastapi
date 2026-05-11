from sqlalchemy import Column, Integer, String, DateTime # Tipos de dados das colunas
from datetime import datetime # Para marcar a hora da consulta
from .database import Base # Importa a base que criamos no database.py

class CEPRecord(Base):
    __tablename__ = "consultas_cep" # Nome da tabela no MySQL

    id = Column(Integer, primary_key=True, index=True) # Identificador único
    cep = Column(String(10), unique=True, index=True) # O CEP buscado (não pode repetir)
    logradouro = Column(String(100)) # Rua/Avenida
    bairro = Column(String(50)) # Bairro
    cidade = Column(String(50)) # Cidade
    estado = Column(String(2)) # UF (MG, SP, etc)
    data_consulta = Column(DateTime, default=datetime.utcnow) # Hora que foi salvo