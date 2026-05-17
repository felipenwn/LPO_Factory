import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.locacao_dao import LocacaoDAO
from dao.veiculo_dao import VeiculoDAO
from model.locacao import locacao
from model.status_locacao import StatusLocacao
from datetime import date
from model.categoria import categoria

class LocacaoController:
    def __init__(self):
        self.locacao_dao = LocacaoDAO()
        self.veiculo_dao = VeiculoDAO()

    def salvar_locacao(self, data_inicio: date, data_fim: date, placa_veiculo: str, status_str: str = "reservado"):
        try:
            if data_fim < data_inicio:
                return False, "Data de devolução não pode ser anterior à data de início."
            
            veiculo = self.veiculo_dao.buscar_por_placa(placa_veiculo)
            if not veiculo:
                return False, "Veículo não encontrado."

            status_enum = StatusLocacao(status_str.lower())
            nova_locacao = locacao(data_inicio, data_fim, veiculo, status=status_enum)
            
            return self.locacao_dao.salvar(nova_locacao)
        except ValueError:
            return False, "Status inválido."
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def listar_locacoes(self):
        return self.locacao_dao.listar_todos()

    def buscar_por_id(self, locacao_id: int):
        return self.locacao_dao.buscar_por_id(locacao_id)

    def atualizar_locacao(self, locacao_id: int, data_inicio: date, data_fim: date, placa_veiculo: str, status_str: str):
        try:
            if data_fim < data_inicio:
                return False, "Data de devolução não pode ser anterior à data de início."
                
            veiculo = self.veiculo_dao.buscar_por_placa(placa_veiculo)
            if not veiculo:
                return False, "Veículo não encontrado."

            status_enum = StatusLocacao(status_str.lower())
            locacao_atualizada = locacao(data_inicio, data_fim, veiculo, status=status_enum, id=locacao_id)
            
            return self.locacao_dao.atualizar(locacao_atualizada)
        except Exception as e:
            return False, f"Erro inesperado: {e}"

    def remover_locacao(self, locacao_id: int):
        return self.locacao_dao.remover(locacao_id)

    def buscar_veiculos_disponiveis(self, data_inicio: date, data_fim: date, categoria_str: str):
        try:
            cat_enum = categoria[categoria_str.upper()]
            return self.locacao_dao.buscar_veiculos_disponiveis(data_inicio, data_fim, cat_enum)
        except KeyError:
            print("Categoria inválida.")
            return []

    # Regras de Negócio - Ações do Usuário

    def locar_veiculo(self, locacao_id: int):
        loc = self.buscar_por_id(locacao_id)
        if not loc:
            return False, "Locação não encontrada."
        
        if loc.status != StatusLocacao.RESERVADO:
            return False, "Apenas locações reservadas podem ser locadas."
            
        # Atualiza a data_inicio para hoje se for diferente
        hoje = date.today()
        if loc.data_inicio != hoje:
            loc.data_inicio = hoje
            
        loc.status = StatusLocacao.LOCADO
        return self.locacao_dao.atualizar(loc)

    def devolver_veiculo(self, locacao_id: int):
        loc = self.buscar_por_id(locacao_id)
        if not loc:
            return False, "Locação não encontrada.", None
            
        if loc.status != StatusLocacao.LOCADO:
            return False, "Apenas veículos locados podem ser devolvidos.", None
            
        hoje = date.today()
        if loc.data_inicio > hoje:
            return False, "Erro: Data de início é no futuro. Não pode devolver.", None
            
        loc.data_fim = hoje
        loc.status = StatusLocacao.DEVOLVIDO
        
        sucesso, msg = self.locacao_dao.atualizar(loc)
        return sucesso, msg, loc

    def cancelar_reserva(self, locacao_id: int):
        loc = self.buscar_por_id(locacao_id)
        if not loc:
            return False, "Locação não encontrada."
            
        if loc.status != StatusLocacao.RESERVADO:
            return False, "Apenas reservas podem ser canceladas."
            
        loc.status = StatusLocacao.CANCELADO
        return self.locacao_dao.atualizar(loc)
