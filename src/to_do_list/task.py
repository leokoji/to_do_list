from enum import Enum
from datetime import date


class Status(Enum):
    CONCLUIDA = "concluida"
    PENDENTE = "pendente"

class Tipo(Enum):
    UNICA = "unica"
    RECORRENTE = "recorrente"

class Task:
    def __init__(self,titulo,descricao,tipo,periodo=None):
        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo 
        self.periodo = periodo
        self.data_criacao = date.today()
        self.data_conclusao = None
        self.status = Status.PENDENTE
        self.id = None

        if self.tipo == Tipo.UNICA:
            self.periodo = None
        elif self.tipo == Tipo.RECORRENTE:
            if self.periodo is None:
                raise ValueError("Insira um valor entre 1 e 365")
            elif not isinstance(self.periodo, int):
                raise ValueError("Insira um valor entre 1 e 365")
            elif self.periodo < 1 or self.periodo > 365:
                raise ValueError("Insira um numero inteiro valido.")
                            
        if not isinstance(tipo,Tipo):
            raise ValueError("Insira uma opção entre recorrente e unica")

        if not titulo.strip():
            raise ValueError("Insira alguma coisa no campo titulo")

        if not descricao.strip():
            raise ValueError("Insira alguma coisa no campo descrição.")

    def exibir(self):
        print(f"""
        Titulo: {self.titulo}
        Descrição: {self.descricao}
        Tipo: {self.tipo}
        Periodo: {self.periodo}
        Criado em: {self.data_criacao}
        Concluido em: {self.data_conclusao}
        Status: {self.status}
        """)

    def concluir(self):
        self.status = Status.CONCLUIDA
        self.data_conclusao = date.today()

    