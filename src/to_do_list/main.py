import flet as ft

def main(page: ft.Page):
    page.title = "To-do List de Estudos"
    page.add(
        ft.Text("To-do List de Estudoss"),
    )

if __name__ == "__main__":
    ft.run(main)

    task1 = Task("tarefa", "isso é uma tarefa", Tipo.UNICA)

    task2 = Task("segunda tarefa", "essa é a segunda tarefa", Tipo.RECORRENTE, 354)
    print("antes de concluir")
    task1.exibir()

    task1.concluir()
    print("depois de concluir")
    task1.exibir()