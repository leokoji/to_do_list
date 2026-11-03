import sqlite3
from pathlib import Path
from to_do_list.task import Task, Tipo, Status, date

DB_PATH = Path("task.db")

def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            status TEXT NOT NULL,
            periodo INTEGER,
            data_criacao TEXT NOT NULL,
            data_conclusao TEXT
        )
    """)
    conn.commit()
    conn.close()

def criar_historico():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historico(
            id_historico INTEGER PRIMARY KEY AUTOINCREMENT,
            id_task INTEGER,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            data_conclusao TEXT
        )
    """)
    conn.commit()
    conn.close()

def registrar_historico(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO historico (id_task, titulo, descricao, data_criacao, data_conclusao)
        SELECT id,titulo, descricao, data_criacao, data_conclusao
        FROM task
        WHERE Id = ?
    """, (task_id,))

    conn.commit()
    conn.close()

def criar_tarefa(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO task(
            titulo,
            descricao,
            tipo,
            periodo,
            status,
            data_criacao,
            data_conclusao)
            VALUES (?,?,?,?,?,?,?)
    """, (task.titulo,task.descricao,task.tipo.value,task.periodo,task.status.value,task.data_criacao.isoformat(),None,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id

def editar_tarefa(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE task SET titulo = ? , descricao = ?, tipo = ?, periodo = ? WHERE id = ?""", 
        (task.titulo, task.descricao, task.tipo.value, task.periodo, task.task_id))

    conn.commit()
    conn.close()

def concluir_tarefa(task):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE task SET data_conclusao = ?, status = ? WHERE id = ?
    """,(task.data_conclusao.isoformat(), task.status.value, task.task_id))

    conn.commit()
    conn.close()

    registrar_historico(task.task_id)

def listar_tarefas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, descricao, tipo, periodo, status,
               data_criacao, data_conclusao
        FROM task
    """)

    linhas_task = cursor.fetchall()
    conn.close()
    return linhas_task

def listar_historico():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
    """
        SELECT id_historico, id_task, titulo, descricao,
            data_criacao, data_conclusao
        FROM historico
    """)

    linhas_historico = cursor.fetchall()
    conn.close()
    return linhas_historico

def excluir_tarefa(task_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM task WHERE id = ?
        """,(task_id,)
    )

    conn.commit()
    conn.close()


def inicializar():
    linhas = listar_tarefas()
    lista_task = []

    for i in linhas:
        task_id = i[0]
        titulo = i[1]
        descricao = i[2]
        
        if i[3] == Tipo.UNICA.value:
            tipo = Tipo.UNICA
        elif i[3] == Tipo.RECORRENTE.value:
            tipo = Tipo.RECORRENTE
        else:
            raise ValueError("Dado Invalido")

        periodo = i[4]

        if i[5] == Status.CONCLUIDA.value:
            status = Status.CONCLUIDA
        elif i[5] == Status.PENDENTE.value:
            status = Status.PENDENTE
        else:
            raise ValueError("Dado invalido")

        data_criacao = date.fromisoformat(i[6])

        if i[7] is None:
            data_conclusao = None
        elif i[7] is not None:
            data_conclusao = date.fromisoformat(i[7])

        task = Task(titulo,descricao,task_id,tipo,status,periodo,data_criacao, data_conclusao)
        lista_task.append(task)
    return lista_task

def adicionar_itens_teste():
    task = Task("item3","issoéumteste3")
    criar_tarefa(task)