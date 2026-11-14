import flet as ft
from to_do_list.task import Task, Tipo, Status
from to_do_list import database


def input_box():
    return ft.TextField(
            border=ft.OutlineInputBorder(
                border_radius=12,
                side=ft.BorderSide(width=5, color="grey"),
                ),
                content_padding = 5
                )


def main(page:ft.Page):

    lista_tarefas = database.inicializar()
    #Caixa do Periodo
    periodo_text = ft.Text("Periodo", visible = False)
    periodo_box = input_box()
    periodo_box.visible = False
    periodo_box.width = 150

    #Caixa da descrição
    descricao_box = input_box()
    descricao_box.multiline = True
    descricao_box.width = 400
    descricao_box.min_lines = 2

    #Caixa do titlo
    titulo_box = input_box()
    titulo_box.width = 400

    aviso_atualizacao_tarefa = ft.Text()

    def tipo_alterado(e):
        periodo_text.visible = e.control.value == Tipo.RECORRENTE.value
        periodo_box.visible = e.control.value == Tipo.RECORRENTE.value
        page.update()   

    #Caida do tipo
    tipo_box = ft.RadioGroup(
        content = ft.Row(
            controls = [
                ft.Text("Tipo"),
                ft.Radio(value=Tipo.UNICA.value, label='Unica'),
                ft.Radio(value=Tipo.RECORRENTE.value, label="Recorrente")]), 
                on_change = tipo_alterado)

    def gerar_cartoes():
        cartoes = []
        for tarefa in lista_tarefas:
            menu_opcoes_tarefa = ft.PopupMenuButton(
                content=ft.Text("..."),
                items=[
                    ft.PopupMenuItem(
                        content=ft.Text("Editar"),
                        on_click = lambda e, tarefa=tarefa: mostrar_janela_editar_tarefa(e, tarefa),
                    ),
                    ft.PopupMenuItem(
                        content=ft.Text("Deletar"),
                        on_click = lambda e, tarefa=tarefa: mostrar_janela_excluir_tarefa(e, tarefa),
                    ),
                ],
            )
            checkbox_status = ft.Checkbox(label="Concluida")
            card = ft.Card(
                content = ft.Column(
                    controls = [
                    ft.Row(
                        controls = [
                        ft.Text(tarefa.titulo),
                        menu_opcoes_tarefa,
                        ],alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Column(
                        controls = [
                            ft.Text(tarefa.descricao),
                        ],
                    ),
                    ft.Row(
                        controls = [
                            checkbox_status,
                        ],
                    ),
                    ]))
            cartoes.append(card)
        return cartoes

    def criar_Tarefa(e):
        try:
            titulo = titulo_box.value    

            descricao = descricao_box.value

            if tipo_box.value == Tipo.UNICA.value:
                tipo = Tipo.UNICA
                periodo = periodo_box.value
            elif tipo_box.value is None:
                tipo = None
                periodo = periodo_box.value
            elif tipo_box.value == Tipo.RECORRENTE.value:
                tipo = Tipo.RECORRENTE
                periodo = int(periodo_box.value)

            task = Task(titulo, descricao, tipo = tipo, periodo = periodo)
            task_id = database.criar_tarefa(task)
            task.task_id = task_id
            lista_tarefas.append(task)
        
            titulo_box.value = None
            descricao_box.value = None
            tipo_box.value = None
            periodo_box.value = None

            aviso_atualizacao_tarefa.color = "green"
            aviso_atualizacao_tarefa.value = "Tarefa inclusa!"

            tarefas.controls = gerar_cartoes()
            page.update()
            
        except ValueError as erro:
            print(str(erro))
            aviso_atualizacao_tarefa.color = "red"
            aviso_atualizacao_tarefa.value = str(erro)

    page.title = "To Do List"
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = True

    def editar_tarefa(e):
        try:
            titulo = titulo_box.value    
            descricao = descricao_box.value

            if tipo_box.value == Tipo.UNICA.value:
                tipo = Tipo.UNICA
                periodo = periodo_box.value
            elif tipo_box.value is None:
                tipo = None
                periodo = periodo_box.value
            elif tipo_box.value == Tipo.RECORRENTE.value:
                tipo = Tipo.RECORRENTE
                periodo = int(periodo_box.value)

            tarefa_edicao.editar(titulo,descricao,tipo,periodo)
            database.editar_tarefa(tarefa_edicao)

            tarefa_edicao.titulo = titulo
            tarefa_edicao.descricao = descricao
            tarefa_edicao.tipo = tipo
            tarefa_edicao.periodo = periodo

            aviso_atualizacao_tarefa.color = "green"
            aviso_atualizacao_tarefa.value = "Tarefa editada!"

            tarefas.controls = gerar_cartoes()
            page.update()
            
        except ValueError as erro:
            print(str(erro))
            aviso_atualizacao_tarefa.color = "red"
            aviso_atualizacao_tarefa.value = str(erro)   
        except TypeError:
            print("Você deve inserir um valor em periodo.")
            aviso_atualizacao_tarefa.color = "red"
            aviso_atualizacao_tarefa.value = "voce deve inserir um valor em periodo."


    tarefa_edicao = None
    def mostrar_janela_editar_tarefa(e, tarefa):
        nonlocal tarefa_edicao
        tarefa_edicao = tarefa
        titulo_box.value = tarefa.titulo
        descricao_box.value = tarefa.descricao
        periodo_box.value = tarefa.periodo
        tipo_box.value = tarefa.tipo.value   

        page.show_dialog(janela_editar_tarefa)
 

    janela_editar_tarefa = ft.AlertDialog(        
        title = ft.Row( controls = [
            ft.Text("Detalhes da tarefa"),
            ft.TextButton("x", on_click = lambda e: page.pop_dialog())
        ],
        alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

        content = ft.Container(
            ft.Column(
                controls = [
                    ft.Text("titulo"),
                    titulo_box,

                    ft.Text("Descrição"),
                    descricao_box,

                    tipo_box,

                    periodo_text,
                    periodo_box,

                    aviso_atualizacao_tarefa,
                ],
            ),
            height = 400,
            width = 400),
        actions = [
            ft.TextButton("Salvar", on_click = editar_tarefa)
        ]
    )

    janela_criar_tarefa = ft.AlertDialog(
        title = ft.Row( controls = [
        ft.Text("Detalhes Da Tarefa"), 
        ft.TextButton("x", on_click = lambda a: page.pop_dialog())], 
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

        content = ft.Container(
            ft.Column(
                controls = [
                    ft.Text("Titulo"),
                    titulo_box,
                    
                    ft.Text("Descricao"),
                    descricao_box,
                
                    tipo_box,

                    periodo_text,
                    periodo_box,

                    aviso_atualizacao_tarefa,
                    ],
                    
                    ),
                    height = 400,
                    width = 400),
        actions = [
            ft.TextButton("Salvar", on_click = criar_Tarefa)
        ],)

    def excluir_tarefa(e):
        id_task = tarefa_exclusao.task_id

        database.excluir_tarefa(id_task)
        lista_tarefas.remove(tarefa_exclusao)

        tarefas.controls = gerar_cartoes()
        page.update()
        page.pop_dialog()

    janela_excluir_tarefa = ft.AlertDialog(
        title = ft.Row( controls = [
            ft.Text("Tem certeza que deseja excluir a tarefa?", color="red")],
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            ),

            content = ft.Container(
                ft.Row(
                    controls = [
                        ft.TextButton("Sim.", on_click = excluir_tarefa),
                        ft.TextButton("Não.", on_click = lambda a: page.pop_dialog())      
                        ]
                )
            )
    )

    tarefa_exclusao = None
    def mostrar_janela_excluir_tarefa(e, tarefa):
        nonlocal tarefa_exclusao
        tarefa_exclusao = tarefa
        page.show_dialog(janela_excluir_tarefa)

    def mostrar_aba_criar_tarefa(e):
        page.show_dialog(janela_criar_tarefa)

    cabecalho = ft.Card (
        content = ft.Container(
        content = ft.Row(
            controls=[
                ft.Text("   To Do List Pessoal", size = 24,),
                ft.Button("+", height = 80, width = 80,
                on_click = mostrar_aba_criar_tarefa,
                style = ft.ButtonStyle(
                    text_style=ft.TextStyle(size = 34))),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        ),
            height = 100,
    )

    tarefas = ft.Column(controls=gerar_cartoes(), scroll = ft.ScrollMode.AUTO, expand = True)


    page.add(cabecalho)
    page.add(tarefas)


if __name__ == "__main__":
    ft.run(main)

