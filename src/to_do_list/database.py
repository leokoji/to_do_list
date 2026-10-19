import sqlite3

def criar_tabela():
    conn = sqlite3.connect("task.db")
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

def criar_tarefa(task):
    conn = sqlite3.connect("task.db")
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
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE task SET titulo = ? , descricao = ?, tipo = ?, periodo = ? WHERE id = ?""", 
        (task.titulo, task.descricao, task.tipo.value, task.periodo, task.id))

    conn.commit()
    conn.close()

def concluir_tarefa(task):
    conn = sqlite3.connect("task.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE task SET data_conclusao = ?, status = ? WHERE id = ?
    """,(task.data_conclusao.isoformat(), task.status, task.id))
    
    conn.commit()
    conn.close()