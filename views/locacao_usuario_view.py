import tkinter as tk
from tkinter import Button, Label, Listbox, Frame, messagebox, Toplevel, Entry, ttk
from control.locacao_controller import LocacaoController
from datetime import datetime, date
from model.categoria import categoria

class JanelaLocacaoUsuario(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Operações de Locação - Usuário")
        self.geometry("650x450")
        
        self.controller = LocacaoController()
        self.locacoes = []
        
        Label(self, text="Operações do Dia a Dia", pady=10).pack()
        
        self.listbox = Listbox(self, width=90, height=15)
        self.listbox.pack(pady=10)
        
        frame_botoes = Frame(self)
        frame_botoes.pack()
        
        Button(frame_botoes, text="Nova Reserva", command=self.acao_nova_reserva).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Ver Detalhes", command=self.acao_detalhes).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Locar", command=self.acao_locar).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Devolver", command=self.acao_devolver).pack(side=tk.LEFT, padx=5)
        Button(frame_botoes, text="Cancelar", command=self.acao_cancelar).pack(side=tk.LEFT, padx=5)
        
        self.carregar_dados()

    def carregar_dados(self):
        self.listbox.delete(0, tk.END)
        self.locacoes = self.controller.listar_locacoes()
        for loc in self.locacoes:
            self.listbox.insert(tk.END, f"ID: {loc.id} | Veículo: {loc.veiculo.placa} | Status: {loc.status.value.upper()} | Início: {loc.data_inicio.strftime('%d/%m/%Y')} | Fim: {loc.data_fim.strftime('%d/%m/%Y')}")

    def acao_nova_reserva(self):
        janela = JanelaNovaReserva(self, self.controller)
        self.wait_window(janela)
        self.carregar_dados()

    def acao_detalhes(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            detalhes = f"ID: {loc.id}\nPlaca: {loc.veiculo.placa}\n"
            
            if loc.status.value == "devolvido":
                detalhes += f"Data Início: {loc.data_inicio.strftime('%d/%m/%Y')}\n"
                detalhes += f"Data Devolução: {loc.data_fim.strftime('%d/%m/%Y')}\n"
                dias = (loc.data_fim - loc.data_inicio).days
                if dias <= 0: dias = 1
                detalhes += f"Número de diárias: {dias}\n"
                detalhes += f"Valor Total: R$ {loc.calcular_valor_locacao():.2f}"
            elif loc.status.value in ["reservado", "locado"]:
                detalhes += f"Data Início: {loc.data_inicio.strftime('%d/%m/%Y')}\n"
                detalhes += f"Data Fim Prevista: {loc.data_fim.strftime('%d/%m/%Y')}\n"
                detalhes += f"Valor Estimado: R$ {loc.calcular_valor_locacao():.2f}"
            elif loc.status.value == "cancelado":
                detalhes += "--- ESTA LOCAÇÃO FOI CANCELADA ---\n"
                detalhes += f"Data Início Prevista: {loc.data_inicio.strftime('%d/%m/%Y')}\n"
                detalhes += f"Data Fim Prevista: {loc.data_fim.strftime('%d/%m/%Y')}"
                
            messagebox.showinfo("Detalhes da Locação", detalhes)
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação.")

    def acao_locar(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            if loc.status.value != "reservado":
                messagebox.showerror("Erro", "Apenas reservas podem ser locadas.")
                return
            
            if messagebox.askyesno("Confirmar", f"Confirmar locação do veículo {loc.veiculo.placa}?"):
                sucesso, msg = self.controller.locar_veiculo(loc.id)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Veículo locado com sucesso.")
                    self.carregar_dados()
                else:
                    messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação.")

    def acao_devolver(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            if loc.status.value != "locado":
                messagebox.showerror("Erro", "Apenas veículos locados podem ser devolvidos.")
                return
                
            if messagebox.askyesno("Confirmar", f"Confirmar devolução do veículo {loc.veiculo.placa}?"):
                sucesso, msg, loc_atualizada = self.controller.devolver_veiculo(loc.id)
                if sucesso:
                    dias = (loc_atualizada.data_fim - loc_atualizada.data_inicio).days
                    if dias <= 0: dias = 1
                    info = f"Devolução realizada!\n\nInício: {loc_atualizada.data_inicio.strftime('%d/%m/%Y')}\n"
                    info += f"Fim: {loc_atualizada.data_fim.strftime('%d/%m/%Y')}\n"
                    info += f"Diárias: {dias}\n"
                    info += f"Total a pagar: R$ {loc_atualizada.calcular_valor_locacao():.2f}"
                    messagebox.showinfo("Recibo de Devolução", info)
                    self.carregar_dados()
                else:
                    messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação.")

    def acao_cancelar(self):
        sel = self.listbox.curselection()
        if sel:
            loc = self.locacoes[sel[0]]
            if loc.status.value != "reservado":
                messagebox.showerror("Erro", "Apenas reservas podem ser canceladas.")
                return
                
            if messagebox.askyesno("Confirmar", f"Confirmar cancelamento da reserva do veículo {loc.veiculo.placa}?"):
                sucesso, msg = self.controller.cancelar_reserva(loc.id)
                if sucesso:
                    messagebox.showinfo("Sucesso", "Reserva cancelada.")
                    self.carregar_dados()
                else:
                    messagebox.showerror("Erro", msg)
        else:
            messagebox.showwarning("Aviso", "Selecione uma locação.")


class JanelaNovaReserva(tk.Toplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.title("Nova Reserva")
        self.geometry("400x450")
        
        Label(self, text="Categoria Desejada:").pack(pady=5)
        self.cb_categoria = ttk.Combobox(self, values=["ECONOMICO", "EXECUTIVO"], state="readonly")
        self.cb_categoria.pack()
        
        Label(self, text="Data Início (DD/MM/AAAA):").pack(pady=5)
        self.txt_inicio = Entry(self)
        self.txt_inicio.pack()
        
        Label(self, text="Data Fim (DD/MM/AAAA):").pack(pady=5)
        self.txt_fim = Entry(self)
        self.txt_fim.pack()
        
        Button(self, text="Buscar Veículos", command=self.buscar_veiculos).pack(pady=10)
        
        Label(self, text="Veículos Disponíveis:").pack(pady=5)
        self.cb_veiculo = ttk.Combobox(self, state="readonly")
        self.cb_veiculo.pack()
        
        Button(self, text="Confirmar Reserva", command=self.confirmar).pack(pady=20)
        
    def buscar_veiculos(self):
        cat = self.cb_categoria.get()
        str_inicio = self.txt_inicio.get()
        str_fim = self.txt_fim.get()
        
        if not cat or not str_inicio or not str_fim:
            messagebox.showwarning("Aviso", "Preencha categoria e datas para buscar.")
            return
            
        try:
            d_inicio = datetime.strptime(str_inicio, '%d/%m/%Y').date()
            d_fim = datetime.strptime(str_fim, '%d/%m/%Y').date()
            
            if d_fim < d_inicio:
                messagebox.showerror("Erro", "Data de devolução menor que a de início.")
                return
                
            veiculos = self.controller.buscar_veiculos_disponiveis(d_inicio, d_fim, cat)
            placas = [v.placa for v in veiculos]
            
            self.cb_veiculo['values'] = placas
            if placas:
                self.cb_veiculo.set(placas[0])
                messagebox.showinfo("Resultado", f"{len(placas)} veículo(s) disponível(is).")
            else:
                self.cb_veiculo.set('')
                messagebox.showinfo("Resultado", "Nenhum veículo disponível nesse período.")
                
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA.")

    def confirmar(self):
        placa = self.cb_veiculo.get()
        str_inicio = self.txt_inicio.get()
        str_fim = self.txt_fim.get()
        
        if not placa:
            messagebox.showerror("Erro", "Selecione um veículo.")
            return
            
        try:
            d_inicio = datetime.strptime(str_inicio, '%d/%m/%Y').date()
            d_fim = datetime.strptime(str_fim, '%d/%m/%Y').date()
            
            sucesso, msg = self.controller.salvar_locacao(d_inicio, d_fim, placa, "reservado")
            
            if sucesso:
                messagebox.showinfo("Sucesso", "Reserva confirmada!")
                self.destroy()
            else:
                messagebox.showerror("Erro", msg)
                
        except ValueError:
            messagebox.showerror("Erro", "Dados inválidos.")
