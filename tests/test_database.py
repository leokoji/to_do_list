import sqlite3
from datetime import date

from to_do_list import database
from to_do_list.task import Task,Status, Tipo


def test_listar_tarefas_retorna_linhas_do_banco(tmp_path, monkeypatch):
    database_path = tmp_path / "tasks.db"
    monkeypatch.setattr(database, "DB_PATH", database_path)

    with sqlite3.connect(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE task (
                id INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                status TEXT NOT NULL,
                periodo INTEGER,
                data_criacao TEXT NOT NULL,
                data_conclusao TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO task (
                id, titulo, descricao, tipo, status,
                periodo, data_criacao, data_conclusao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (7, "Estudar", "Revisar banco", "unica", "pendente", None, "2026-10-23", None),
        )

    linhas = database.listar_tarefas()

    assert linhas == [
        (7, "Estudar", "Revisar banco", "unica", None, "pendente", "2026-10-23", None)
    ]

    
def test_inicializar_sistema(tmp_path, monkeypatch):
    database_path = tmp_path / "tasks.db"
    monkeypatch.setattr(database, "DB_PATH", database_path)

    with sqlite3.connect(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE task (
                id INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                periodo INTEGER,
                status TEXT NOT NULL,
                data_criacao TEXT NOT NULL,
                data_conclusao TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO task (
                id,titulo,descricao,tipo,periodo,status,data_criacao,data_conclusao)
                VALUES(?,?,?,?,?,?,?,?)
            """,
            (7, "Estudar", "Revisar banco", Tipo.UNICA.value, None, Status.PENDENTE.value,"2026-10-23", None),
            )
        conn.execute(
            """
            INSERT INTO task (
                id,titulo,descricao,tipo,periodo,status,data_criacao,data_conclusao)
                VALUES(?,?,?,?,?,?,?,?)
            """,
            (12, "Estudar", "Revisar banco", Tipo.RECORRENTE.value, 20, Status.CONCLUIDA.value,"2026-10-23", None),
            )
        conn.execute(
            """
            INSERT INTO task (
                id,titulo,descricao,tipo,periodo,status,data_criacao,data_conclusao)
                VALUES(?,?,?,?,?,?,?,?)
            """,
            (4, "Estudar", "Revisar banco", Tipo.RECORRENTE.value, 100, Status.PENDENTE.value,"2026-10-23", None),
            )

    lista_task = database.inicializar()

    assert len(lista_task) == 3
    assert all(isinstance(task,Task) for task in lista_task)
    assert lista_task[0].task_id == 4
    assert lista_task[0].titulo == "Estudar"
    assert lista_task[0].descricao == "Revisar banco"
    assert lista_task[0].tipo == Tipo.RECORRENTE
    assert lista_task[0].periodo == 100
    assert lista_task[0].status == Status.PENDENTE
    assert isinstance(lista_task[0].data_criacao, date)
    assert lista_task[0].data_conclusao is None

def test_consultar_historico(tmp_path, monkeypatch):
    database_path = tmp_path / "tasks.db"
    monkeypatch.setattr(database, "DB_PATH", database_path)
    
    database.criar_tabela()
    database.criar_historico()

    titulo = "Estudar"
    descricao = "Estudar programação 1x ao dia"

    task = Task(titulo, descricao, tipo=Tipo.RECORRENTE, periodo=1)
    task.task_id = database.criar_tarefa(task)

    task.concluir()
    database.concluir_tarefa(task)

    linhas_historico = database.listar_historico()

    assert linhas_historico[0][0] == 1
    assert linhas_historico[0][1] == 1
    assert linhas_historico[0][2] == titulo
    assert linhas_historico[0][3] == descricao
    assert date.fromisoformat(linhas_historico[0][4]) == task.data_criacao
    assert date.fromisoformat(linhas_historico[0][5]) == task.data_conclusao

def test_excluir_tarefa(tmp_path, monkeypatch):
    database_path = tmp_path / "task.db"
    monkeypatch.setattr(database, "DB_PATH", database_path)

    database.criar_tabela()
    titulo = "Estudar"
    descricao = "estttudar"

    task = Task(titulo, descricao)
    task.task_id = database.criar_tarefa(task)

    titulo = "Ee"
    descricao = "ii"

    task = Task(titulo,descricao)
    task.task_id = database.criar_tarefa(task)

    lista = database.listar_tarefas()

    assert len(lista) == 2

    database.excluir_tarefa(task.task_id)
    lista = database.listar_tarefas()

    assert len(lista) == 1

def test_editar_tarefa(tmp_path, monkeypatch):
    database_path = tmp_path / "task.db"
    monkeypatch.setattr(database, "DB_PATH", database_path)

    database.criar_tabela()
    titulo = "Estudar"
    descricao = "EEstudar"

    task = Task(titulo, descricao)
    task.task_id = database.criar_tarefa(task)
    lista = database.listar_tarefas()

    assert lista[0][1] == titulo
    assert lista[0][2] == descricao

    titulo1 = "mudei as coisa"
    descricao1 = "mudei otas coisa"
    tipo = Tipo.UNICA

    task.editar(titulo1, descricao1, tipo)
    database.editar_tarefa(task)
    lista = database.listar_tarefas()

    assert lista[0][1] == titulo1
    assert lista[0][2] == descricao1


