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