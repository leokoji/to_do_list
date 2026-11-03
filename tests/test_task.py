from to_do_list.task import Status, Task, Tipo
from datetime import date

def test_tarefa_unica_comeca_pendente_sem_data_de_conclusao():
    task = Task("Estudar Python", "Revisar classes", Tipo.UNICA)

    assert task.status == Status.PENDENTE
    assert task.data_conclusao is None

def test_tarefa_unica_pendente_e_concluida():
    task = Task("Teste", "Teste", Tipo.UNICA)
    task.concluir()

    assert task.status == Status.CONCLUIDA
    assert task.data_conclusao is not None

def test_edição_tarefa():
    titulo = "Estudar python"
    descricao = "Revisar classes"
    tipo = Tipo.RECORRENTE
    periodo = 3

    task = Task(titulo, descricao, tipo=tipo, periodo=periodo)
    assert task.titulo == titulo
    assert task.descricao == descricao
    assert task.tipo == tipo
    assert task.periodo == periodo
    
    titulo = "Não estudar tarefa"
    descricao = "Não revisar classes"
    tipo = Tipo.UNICA
    periodo = None

    task.editar(titulo, descricao, tipo)
    assert task.titulo == titulo
    assert task.descricao == descricao
    assert task.tipo == tipo
    assert task.periodo is None

