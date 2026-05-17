import tkinter as tk
from tkinter import Button, Label, Listbox, Frame, messagebox
from views.veiculo_form_view import abrir_formulario
from control.veiculo_controller import VeiculoController

def abrir_lista_veiculos(janela_pai):
    janela = tk.Toplevel(janela_pai)
    janela.title("Veículos Cadastrados")
    janela.geometry("500x400")

    controller = VeiculoController()
    veiculos_carregados = [] # Lista local para espelhar a listbox

    lbl_titulo = Label(janela, text="Veículos Cadastrados", pady=10)
    lbl_titulo.pack()

    listbox_veiculos = Listbox(janela, width=60, height=12)
    listbox_veiculos.pack()

    frame_botoes = Frame(janela, pady=15)
    frame_botoes.pack()

    def atualizar_listbox():
        nonlocal veiculos_carregados
        listbox_veiculos.delete(0, tk.END)
        veiculos_carregados = controller.listar_veiculos()
        for v in veiculos_carregados:
            listbox_veiculos.insert(tk.END, f"Placa: {v.placa} | Tipo: {type(v).__name__.capitalize()} | Categoria: {v.categoria.name}")

    def acao_novo():
        abrir_formulario(janela, controller, atualizar_listbox)
        # O fluxo já é tratado pelo callback_atualizar na tela de form, não precisa wait_window aqui pois o callback já recarrega

    def acao_editar():
        selecionado = listbox_veiculos.curselection()
        if selecionado:
            index = selecionado[0]
            veiculo_selecionado = veiculos_carregados[index]
            abrir_formulario(janela, controller, atualizar_listbox, veiculo_edicao=veiculo_selecionado)
        else:
            messagebox.showerror("Aviso", "Selecione um veículo na lista para editar!")

    def acao_ver_info():
        selecionado = listbox_veiculos.curselection() 
        if selecionado:
            index = selecionado[0]
            veiculo_selecionado = veiculos_carregados[index]
            dados_formatados = veiculo_selecionado.exibir_dados()
            messagebox.showinfo("Informações do Veículo", dados_formatados)
        else:
            messagebox.showerror("Aviso", "Selecione um veículo na lista!")

    def acao_remover():
        selecionado = listbox_veiculos.curselection()
        if selecionado:
            index = selecionado[0]
            veiculo_selecionado = veiculos_carregados[index]
            
            # Pede confirmação
            resposta = messagebox.askyesno("Confirmar", f"Deseja realmente remover o veículo {veiculo_selecionado.placa}?")
            if resposta:
                sucesso, msg = controller.remover_veiculo(veiculo_selecionado.placa)
                if sucesso:
                    messagebox.showinfo("Sucesso", msg)
                    atualizar_listbox()
                else:
                    messagebox.showerror("Erro", msg)
        else:
            messagebox.showerror("Aviso", "Selecione um veículo para remover!")

    btn_novo = Button(frame_botoes, text="Novo", command=acao_novo)
    btn_novo.pack(side=tk.LEFT, padx=5)

    btn_editar = Button(frame_botoes, text="Editar", command=acao_editar)
    btn_editar.pack(side=tk.LEFT, padx=5)

    btn_info = Button(frame_botoes, text="Ver Informações", command=acao_ver_info)
    btn_info.pack(side=tk.LEFT, padx=5)

    btn_remover = Button(frame_botoes, text="Remover", command=acao_remover)
    btn_remover.pack(side=tk.LEFT, padx=5)

    # Carrega a lista inicial do BD
    atualizar_listbox()