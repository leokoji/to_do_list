import flet as ft
from to_do_list import database, task

def main(page: ft.Page):
    page.title = "To-do List de Estudos"
    page.add(
        ft.Text("To-do List de Estudoss"),
    )

if __name__ == "__main__":
    ft.run(main)

    criar_tabela()
    criar_historico()