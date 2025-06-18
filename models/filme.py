from datetime import date
from enum import Enum

from models.pessoa import Pessoa

class Classificacao(Enum):
    LIVRE = "L"
    DEZ_ANOS = "10"
    DOZE_ANOS = "12"
    QUATORZE_ANOS = "14"
    DEZESSEIS_ANOS = "16"
    DEZOITO_ANOS = "18"

class Genero(Enum):
    ACAO = "Ação"
    AVENTURA = "Aventura"
    COMEDIA = "Comédia"
    DRAMA = "Drama"
    FANTASIA = "Fantasia"
    FICCAO_CIENTIFICA = "Ficção Científica"
    ROMANCE = "Romance"
    TERROR = "Terror"
    GUERRA =  "Guerra"
    ANIMACAO = "Animação"
    DOCUMENTARIO = "Documentário"
    MUSICAL = "Musical"
    SUSPENSE = "Suspense"


class Filme:
    def __init__ (self, 
                    id: int, 
                    titulo: str, 
                    ano_producao: int, 
                    duracao: int, 
                    estreia: date, 
                    genero: list['Genero'], 
                    classificacao: 'Classificacao',
                    diretor: 'Pessoa' = None,
                    nota_media: float = None,
                    pais_origem: list[str] = None, 
                    sinopse: str = None, 
                    total_votos: int = None, 
                    poster_url: str = None, 
                    elenco: list['Pessoa'] = None,
                    roteiristas: list['Pessoa'] = None,
                    produtores: list['Pessoa'] = None): 
        self.id: int = id
        self.titulo: str = titulo
        self.ano_producao: int = ano_producao
        self.duracao: int = duracao
        self.estreia: date = estreia
        self.pais_origem: list[str] = pais_origem
        self.sinopse: str = sinopse
        self.genero: list[Genero] = genero
        self.poster_url: str = poster_url
        self.classificacao: Classificacao = classificacao
        self.diretor: 'Pessoa' = diretor
        self.nota_media = nota_media
        self.total_votos = total_votos
        self.elenco: list[Pessoa] = elenco
        self.roteiristas: list[Pessoa] = roteiristas
        self.produtores: list[Pessoa] = produtores
    

    