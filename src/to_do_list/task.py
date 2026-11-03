from enum import Enum
from datetime import date


class Status(Enum):
    CONCLUIDA = "concluida"
    PENDENTE = "pendente"

class Tipo(Enum):
    UNICA = "unica"
    RECORRENTE = "recorrente"

class Task:
    def __init__(self, titulo, descricao, task_id = None, tipo = Tipo.UNICA, status = Status.PENDENTE, periodo = None, data_criacao = None, data_conclusao = None):
        if data_criacao is None:
            data_criacao = date.today()
        elif isinstance(data_criacao, date):
            data_criacao = data_criacao
        else:
            raise ValueError("Dado de data invalido")

        if tipo == Tipo.UNICA:
            periodo = None
        elif tipo == Tipo.RECORRENTE:
            if periodo is None:
                raise ValueError("Insira um valor entre 1 e 365")
            elif not isinstance(periodo, int):
                raise ValueError("Insira um valor entre 1 e 365")
            elif periodo < 1 or periodo > 365:
                raise ValueError("Insira um numero inteiro valido.")
                            
        if not isinstance(tipo,Tipo):
            raise ValueError("Insira uma opção entre recorrente e unica")

        if not titulo.strip():
            raise ValueError("Insira alguma coisa no campo titulo")

        if not descricao.strip():
            raise ValueError("Insira alguma coisa no campo descrição.")

        self.titulo = titulo
        self.descricao = descricao
        self.task_id = task_id
        self.tipo = tipo
        self.status = status
        self.periodo = periodo
        self.data_criacao = data_criacao
        self.data_conclusao = data_conclusao
        

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
 
    def editar(self, titulo, descricao,tipo,periodo = None):
        if not isinstance(tipo,Tipo):
            raise ValueError("Insira uma opção entre recorrente e unica")

        if not titulo.strip():
            raise ValueError("Insira alguma coisa no campo titulo")

        if not descricao.strip():
            raise ValueError("Insira alguma coisa no campo descrição.")

        if self.tipo == Tipo.UNICA:
            self.periodo = None
        elif self.tipo == Tipo.RECORRENTE:
            if self.periodo is None:
                raise ValueError("Insira um valor entre 1 e 365")
            elif not isinstance(self.periodo, int):
                raise ValueError("Insira um valor entre 1 e 365")
            elif self.periodo < 1 or self.periodo > 365:
                raise ValueError("Insira um numero inteiro valido.")

        self.titulo = titulo
        self.descricao = descricao
        self.tipo = tipo
        self.periodo = periodo