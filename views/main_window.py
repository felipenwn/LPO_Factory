import tkinter as tk
from tkinter import Menu, Label
from views.veiculo_list_view import abrir_lista_veiculos

def iniciar_aplicacao():
    janela_principal = tk.Tk()
    janela_principal.title("Locadora de Veículos - Sistema Principal")
    janela_principal.geometry("600x400")
    
    lbl_boas_vindas = Label(janela_principal, text="Bem-vindo ao Sistema da Locadora!", font=("Arial", 16))
    lbl_boas_vindas.pack(pady=50)

    # Cria a barra de menus
    barra_menus = Menu(janela_principal)
    
    # Menu Cadastro
    menu_cadastro = Menu(barra_menus, tearoff=0)
    menu_cadastro.add_command(label="Veículo", command=lambda: abrir_lista_veiculos(janela_principal))
    # Importar lazyly para evitar circular import se houver
    menu_cadastro.add_command(label="Locações (Admin)", command=lambda: abrir_locacoes_admin(janela_principal))
    barra_menus.add_cascade(label="Cadastro", menu=menu_cadastro)
    
    # Menu Ação
    menu_acao = Menu(barra_menus, tearoff=0)
    menu_acao.add_command(label="Locar Veículo", command=lambda: abrir_locacao_usuario(janela_principal))
    barra_menus.add_cascade(label="Ação", menu=menu_acao)
    
    janela_principal.config(menu=barra_menus)
    
    janela_principal.mainloop()

def abrir_locacoes_admin(janela_pai):
    from views.locacao_admin_view import JanelaListagemLocacoes
    JanelaListagemLocacoes(janela_pai)

def abrir_locacao_usuario(janela_pai):
    from views.locacao_usuario_view import JanelaLocacaoUsuario
    JanelaLocacaoUsuario(janela_pai)
