import flet as ft

def main(page: ft.Page):
    page.title = "To-do List de Estudos"
    page.add(
        ft.Text("To-do List de Estudoss"),
    )

if __name__ == "__main__":
    ft.run(main)