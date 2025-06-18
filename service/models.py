from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table, Enum, JSON
from sqlalchemy.ext.declarative import declarative_base

from models.filme import Classificacao

Base = declarative_base()

class Filme(Base):
    __tablename__ = 'filmes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    ano_producao = Column(Integer, nullable=False)
    duracao = Column(Integer, nullable=False)
    estreia = Column(DateTime, nullable=False)
    generos = Column(JSON, nullable=True) 
    classificacao = Column(Enum(Classificacao), nullable=False)
    nota_media = Column(Float, nullable=True)
    pais_origem = Column(JSON, nullable=True)
    sinopse = Column(String, nullable=True)
    total_votos = Column(Integer, nullable=True)
    poster_url = Column(String, nullable=True)
    elenco = Column(JSON, nullable=True)
    pessoas_referencias = Column(JSON, nullable=True)
