import tkinter as tk
from tkinter import Button, Label, Listbox, Frame, messagebox
from views.veiculo_form_view import abrir_formulario

lista_veiculos = []

def iniciar_tela_principal():
    janela = tk.Tk()
    janela.title("Locadora de Veículos")
    janela.geometry("450x350")

    lbl_titulo = Label(janela, text="Veículos Cadastrados", pady=10)
    lbl_titulo.pack()

    listbox_veiculos = Listbox(janela, width=50, height=10)
    listbox_veiculos.pack()

    frame_botoes = Frame(janela, pady=15)
    frame_botoes.pack()

    def acao_novo():
        abrir_formulario(janela, lista_veiculos, listbox_veiculos)

    def acao_ver_info():
        selecionado = listbox_veiculos.curselection() 
        if selecionado:
            index = selecionado[0]
            veiculo_selecionado = lista_veiculos[index]
            
            dados_formatados = veiculo_selecionado.exibir_dados()
            
            messagebox.showinfo("Informações do Veículo", dados_formatados)
        else:
            messagebox.showerror("Aviso", "Selecione um veículo na lista!")

    def acao_remover():
        selecionado = listbox_veiculos.curselection()
        if selecionado:
            index = selecionado[0]
            lista_veiculos.pop(index) # Remove da memória
            
            listbox_veiculos.delete(0, tk.END)
            for v in lista_veiculos:
                listbox_veiculos.insert(tk.END, f"Placa: {v.placa} | Tipo: {type(v).__name__}")
        else:
            messagebox.showerror("Aviso", "Selecione um veículo para remover!")

    btn_novo = Button(frame_botoes, text="Novo", command=acao_novo)
    btn_novo.pack(side=tk.LEFT, padx=5) # side=tk.LEFT coloca eles lado a lado

    btn_info = Button(frame_botoes, text="Ver Informações", command=acao_ver_info)
    btn_info.pack(side=tk.LEFT, padx=5)

    btn_remover = Button(frame_botoes, text="Remover", command=acao_remover)
    btn_remover.pack(side=tk.LEFT, padx=5)

    janela.mainloop()