import tkinter as tk
from tkinter import Button, Label, Listbox, Frame, messagebox, Toplevel, Entry, ttk
from control.locacao_controller import LocacaoController
from control.veiculo_controller import VeiculoController
from datetime import datetime

class JanelaListagemLocacoes(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Locações - Administrador")
        self.geometry("600x450")
        
        self.controller = LocacaoController()
        self.locacoes = []
        
        Label(self, text="Gerenciamento de Locações (Irrestrito)", pady=10).pack()
        
        self.listbox = Listbox(self, width=80, height=15)
        self.listbox.pack(pady=10)
        
        frame_botoes = Frame(self)
        frame_botoes.pack()
        
        Button(frame_botoes, text="Nova Locação", command=self.acao_novo).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Editar", command=self.acao_editar).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Ver Detalhes", command=self.acao_detalhes).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Remover", command=self.acao_remover).pack(side=tk.LEFT, padx=5)
        
        self.carregar_dados()

    def carregar_dados(self):
        self.listbox.delete(0, tk.END)
        self.locacoes = self.controller.listar_locacoes()
        for loc in self.locacoes:
            valor_str = f" | R$ {loc.calcular_valor_locacao():.2f}" if loc.status.value == "devolvido" else ""
            self.listbox.insert(tk.END, f"ID: {loc.id} | Veículo: {loc.veiculo.placa} | Status: {loc.status.value.upper()} | Início: {loc.data_inicio.strftime('%d/%m/%Y')}{valor_str}")

    def acao_novo(self):
        janela = JanelaCadastroLocacao(self, self.controller)
        self.wait_window(janela)
        self.carregar_dados()

    def acao_editar(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            janela = JanelaCadastroLocacao(self, self.controller, loc)
            self.wait_window(janela)
            self.carregar_dados()
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação para editar.")

    def acao_detalhes(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            detalhes = f"ID: {loc.id}\nPlaca: {loc.veiculo.placa}\n"
            detalhes += f"Data Início: {loc.data_inicio.strftime('%d/%m/%Y')}\n"
            detalhes += f"Data Fim: {loc.data_fim.strftime('%d/%m/%Y')}\n"
            detalhes += f"Status: {loc.status.value.upper()}\n"
            if loc.status.value == "devolvido":
                detalhes += f"Valor Final: R$ {loc.calcular_valor_locacao():.2f}"
            messagebox.showinfo("Detalhes da Locação", detalhes)
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação.")

    def acao_remover(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            if messagebox.askyesno("Confirmar", f"Remover locação ID {loc.id}?"):
                sucesso, msg = self.controller.remover_locacao(loc.id)
                if sucesso:
                    self.carregar_dados()
                else:
                    messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação.")


class JanelaCadastroLocacao(tk.Toplevel):
    def __init__(self, master, controller, locacao_edicao=None):
        super().__init__(master)
        self.controller = controller
        self.locacao = locacao_edicao
        self.veiculo_controller = VeiculoController()
        
        self.title("Nova Locação" if not locacao_edicao else "Editar Locação")
        self.geometry("350x350")
        
        Label(self, text="Placa do Veículo:").pack(pady=5)
        
        self.veiculos_disponiveis = self.veiculo_controller.listar_veiculos()
        placas = [v.placa for v in self.veiculos_disponiveis]
        
        self.cb_placa = ttk.Combobox(self, values=placas, state="readonly")
        self.cb_placa.pack()
        
        Label(self, text="Data Início (DD/MM/AAAA):").pack(pady=5)
        self.txt_inicio = Entry(self)
        self.txt_inicio.pack()
        
        Label(self, text="Data Fim (DD/MM/AAAA):").pack(pady=5)
        self.txt_fim = Entry(self)
        self.txt_fim.pack()
        
        Label(self, text="Status:").pack(pady=5)
        self.cb_status = ttk.Combobox(self, values=["reservado", "locado", "devolvido", "cancelado"], state="readonly")
        self.cb_status.pack()
        self.cb_status.set("reservado")
        
        if self.locacao:
            self.cb_placa.set(self.locacao.veiculo.placa)
            self.txt_inicio.insert(0, self.locacao.data_inicio.strftime('%d/%m/%Y'))
            self.txt_fim.insert(0, self.locacao.data_fim.strftime('%d/%m/%Y'))
            self.cb_status.set(self.locacao.status.value)
            
        Button(self, text="Salvar", command=self.salvar).pack(pady=20)

    def salvar(self):
        placa = self.cb_placa.get()
        str_inicio = self.txt_inicio.get()
        str_fim = self.txt_fim.get()
        status = self.cb_status.get()
        
        if not placa or not str_inicio or not str_fim or not status:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        try:
            d_inicio = datetime.strptime(str_inicio, '%d/%m/%Y').date()
            d_fim = datetime.strptime(str_fim, '%d/%m/%Y').date()
            
            if self.locacao:
                sucesso, msg = self.controller.atualizar_locacao(self.locacao.id, d_inicio, d_fim, placa, status)
            else:
                sucesso, msg = self.controller.salvar_locacao(d_inicio, d_fim, placa, status)
                
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self.destroy()
            else:
                messagebox.showerror("Erro", msg)
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA.")
