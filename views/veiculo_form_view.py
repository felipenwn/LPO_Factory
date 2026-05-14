import tkinter as tk
from tkinter import Button, Label, Entry, messagebox
from tkinter import ttk

def abrir_formulario(janela_principal, controller, callback_atualizar, veiculo_edicao=None):
    janela = tk.Toplevel(janela_principal)
    janela.geometry("300x400")

    modo_edicao = veiculo_edicao is not None
    if modo_edicao:
        janela.title("Editar Veículo")
    else:
        janela.title("Novo Veículo")

    lbl_placa = Label(janela, text="Informe a Placa:", pady=5)
    lbl_placa.pack()
    txt_placa = Entry(janela)
    txt_placa.pack()

    lbl_tipo = Label(janela, text="Tipo do Veículo:", pady=5)
    lbl_tipo.pack()
    combo_tipo = ttk.Combobox(janela, values=["carro", "motorhome"], state="readonly")
    combo_tipo.pack()

    lbl_categoria = Label(janela, text="Categoria:", pady=5)
    lbl_categoria.pack()
    combo_categoria = ttk.Combobox(janela, values=["ECONOMICO", "EXECUTIVO"], state="readonly")
    combo_categoria.pack()

    lbl_taxa = Label(janela, text="Taxa Diária (R$):", pady=5)
    lbl_taxa.pack()
    txt_taxa = Entry(janela)
    txt_taxa.pack()

    # Preencher os dados se for edição
    if modo_edicao:
        txt_placa.insert(0, veiculo_edicao.placa)
        txt_placa.config(state="disabled") # Não permite alterar a placa na edição
        
        # Pega o tipo exato (ex: Carro -> carro)
        combo_tipo.set(type(veiculo_edicao).__name__.lower())
        combo_categoria.set(veiculo_edicao.categoria.name)
        txt_taxa.insert(0, str(veiculo_edicao.taxa_diaria))

    def salvar_veiculo():
        placa = txt_placa.get()
        tipo = combo_tipo.get()
        categoria_texto = combo_categoria.get()
        taxa_texto = txt_taxa.get()

        if modo_edicao:
            sucesso, msg = controller.atualizar_veiculo(placa, tipo, categoria_texto, taxa_texto)
        else:
            sucesso, msg = controller.salvar_veiculo(placa, tipo, categoria_texto, taxa_texto)

        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            callback_atualizar() # Atualiza a listbox na tela principal
            janela.destroy()
        else:
            messagebox.showerror("Erro", msg)

    btn_texto = "Atualizar" if modo_edicao else "Salvar"
    btn_salvar = Button(janela, text=btn_texto, command=salvar_veiculo, pady=5)
    btn_salvar.pack(pady=15)