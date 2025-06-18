from service.models import Base, Filme
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from service.actors_api import buscar_pessoa_no_master

# Configuração do sqlite

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./movies.db')

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

# ======= CREATE ========
def create_filme(db: Session, filme: Filme):
    db.add(filme)
    db.commit()
    db.refresh(filme)
    return filme

def create_filme_with_pessoas(db: Session, filme_data: dict, pessoas_data: dict):
    try:
        filme = Filme(**filme_data)
        
        pessoas_referencias = {}
        
        if pessoas_data.get('diretor'):
            diretor_info = buscar_pessoa_no_master(pessoas_data['diretor'])
            if diretor_info:
                pessoas_referencias['diretor'] = diretor_info
        
        elenco_info = []
        for nome_ator in pessoas_data.get('elenco', []):
            ator_info = buscar_pessoa_no_master(nome_ator)
            if ator_info:
                elenco_info.append(ator_info)
        if elenco_info:
            pessoas_referencias['elenco'] = elenco_info
        
        roteiristas_info = []
        for nome_roteirista in pessoas_data.get('roteiristas', []):
            roteirista_info = buscar_pessoa_no_master(nome_roteirista)
            if roteirista_info:
                roteiristas_info.append(roteirista_info)
        if roteiristas_info:
            pessoas_referencias['roteiristas'] = roteiristas_info
        
        produtores_info = []
        for nome_produtor in pessoas_data.get('produtores', []):
            produtor_info = buscar_pessoa_no_master(nome_produtor)
            if produtor_info:
                produtores_info.append(produtor_info)
        if produtores_info:
            pessoas_referencias['produtores'] = produtores_info
        
        filme.pessoas_referencias = pessoas_referencias
        
        filme_salvo = create_filme(db, filme)
        
        return filme_salvo
        
    except Exception as e:
        db.rollback()
        raise e

# ======= READ ========

def get_filme_by_id(db: Session, filme_id: int):
    return db.query(Filme).filter(Filme.id == filme_id).first()

def get_filme_by_name(db: Session, titulo: str):
    return db.query(Filme).filter(Filme.titulo.ilike(f"%{titulo}%")).all()

def get_filmes(db: Session):
    return db.query(Filme).filter().all()


# ======= UPDATE ========

def update_filme(db: Session, filme_id: int, filme_data: dict, pessoas_data: dict):
    filme = get_filme_by_id(db, filme_id)
    if not filme:
        raise ValueError("Filme não encontrado")
    
    try:
        for key, value in filme_data.items():
            if hasattr(filme, key):
                setattr(filme, key, value)
        
        pessoas_referencias = {}
        
        if pessoas_data.get('diretor'):
            diretor_info = buscar_pessoa_no_master(pessoas_data['diretor'])
            if diretor_info:
                pessoas_referencias['diretor'] = diretor_info
        
        elenco_info = []
        for nome_ator in pessoas_data.get('elenco', []):
            ator_info = buscar_pessoa_no_master(nome_ator)
            if ator_info:
                elenco_info.append(ator_info)
        if elenco_info:
            pessoas_referencias['elenco'] = elenco_info
        
        roteiristas_info = []
        for nome_roteirista in pessoas_data.get('roteiristas', []):
            roteirista_info = buscar_pessoa_no_master(nome_roteirista)
            if roteirista_info:
                roteiristas_info.append(roteirista_info)
        if roteiristas_info:
            pessoas_referencias['roteiristas'] = roteiristas_info
        
        produtores_info = []
        for nome_produtor in pessoas_data.get('produtores', []):
            produtor_info = buscar_pessoa_no_master(nome_produtor)
            if produtor_info:
                produtores_info.append(produtor_info)
        if produtores_info:
            pessoas_referencias['produtores'] = produtores_info
        
        filme.pessoas_referencias = pessoas_referencias if pessoas_referencias else None
        
        db.commit()
        db.refresh(filme)
        return filme
        
    except Exception as e:
        db.rollback()
        raise e

# ======= DELETE ========

def delete_filme(db: Session, filme_id: int):
    filme = db.query(Filme).filter(Filme.id == filme_id).first()
    db.delete(filme)
    db.commit()
    return filme