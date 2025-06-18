from enum import Enum

class TipoPessoa(Enum):
    DIRETOR = "Diretor"
    ROTEIRISTA = "Roteirista"
    PRODUTOR = "Produtor"
    ATOR = "Ator"

class Pessoa:
    def __init__ (self, id: int, nome: str, foto_url: str, tipo: list[TipoPessoa], filmes: list):
        self.id: int = id
        self.nome: str = nome
        self.foto_url: str = foto_url
        self.tipo: list[TipoPessoa] = tipo
        self.filmes: list = filmes
