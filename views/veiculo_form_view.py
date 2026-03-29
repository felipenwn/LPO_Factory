import tkinter as tk
from tkinter import Button, Label, Entry, messagebox
from tkinter import ttk # Usado para criar as caixinhas de seleção (Combobox)
from model.veiculo_factory import VeiculoFactory
from model.categoria import categoria

def abrir_formulario(janela_principal, lista_veiculos, listbox_veiculos):
    janela = tk.Toplevel(janela_principal)
    janela.title("Novo Veículo")
    janela.geometry("300x400")

    
    lbl_placa = Label(janela, text="Informe a Placa:", pady=5)
    lbl_placa.pack()
    txt_placa = Entry(janela)
    txt_placa.pack()

    lbl_tipo = Label(janela, text="Tipo do Veículo:", pady=5)
    lbl_tipo.pack()
    # Combobox é uma lista suspensa (recomendação da professora no PDF)
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

    def salvar_veiculo():
        placa = txt_placa.get()
        tipo = combo_tipo.get()
        categoria_texto = combo_categoria.get()
        taxa_texto = txt_taxa.get().replace(",", ".") 

        if placa.strip() and tipo.strip() and categoria_texto.strip() and taxa_texto.strip():
            try:
                taxa = float(taxa_texto)
                
                if categoria_texto == "ECONOMICO":
                    cat_enum = categoria.ECONOMICO
                else:
                    cat_enum = categoria.EXECUTIVO

                novo_veiculo = VeiculoFactory.criar_veiculo(tipo, placa, cat_enum, taxa)
                lista_veiculos.append(novo_veiculo)

                listbox_veiculos.delete(0, tk.END)
                for v in lista_veiculos:
                    listbox_veiculos.insert(tk.END, f"Placa: {v.placa} | Tipo: {type(v).__name__}")

                messagebox.showinfo("Sucesso", "Veículo cadastrado!")
                janela.destroy() #
                
            except ValueError:
                messagebox.showerror("Erro", "A taxa diária deve ser um número válido.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro: {e}")
        else:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")

    btn_salvar = Button(janela, text="Salvar", command=salvar_veiculo, pady=5)
    btn_salvar.pack(pady=15)