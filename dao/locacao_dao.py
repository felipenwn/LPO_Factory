import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from model.locacao import locacao
from dao.veiculo_dao import VeiculoDAO
from model.status_locacao import StatusLocacao
from datetime import date

class LocacaoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
        self.veiculo_dao = VeiculoDAO()

    def salvar(self, locacao_obj: locacao):
        if not self.conexao:
            raise Exception("Não foi possível conectar ao banco de dados.")
        try:
            cursor = self.conexao.cursor()
            query = "INSERT INTO tb_locacoes (data_inicio, data_fim, veiculo_placa, status, valor_total) VALUES (%s, %s, %s, %s, %s) RETURNING id"
            
            valor_total = None
            if locacao_obj.status == StatusLocacao.DEVOLVIDO:
                valor_total = locacao_obj.calcular_valor_locacao()
                
            cursor.execute(query, (
                locacao_obj.data_inicio,
                locacao_obj.data_fim,
                locacao_obj.veiculo.placa,
                locacao_obj.status.value,
                valor_total
            ))
            
            # Obtém o ID gerado
            novo_id = cursor.fetchone()[0]
            locacao_obj.id = novo_id
            
            self.conexao.commit()
            return True, "Locação salva com sucesso."
        except Exception as e:
            print(f"Erro ao inserir locação: {e}")
            self.conexao.rollback()
            return False, f"Erro ao salvar locação: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []
        try:
            cursor = self.conexao.cursor()
            query = "SELECT id, data_inicio, data_fim, veiculo_placa, status, valor_total FROM tb_locacoes ORDER BY id DESC"
            cursor.execute(query)
            linhas = cursor.fetchall()
            locacoes = []
            for linha in linhas:
                veiculo = self.veiculo_dao.buscar_por_placa(linha[3])
                if veiculo:
                    status_enum = StatusLocacao(linha[4])
                    loc = locacao(
                        id=linha[0],
                        data_inicio=linha[1],
                        data_fim=linha[2],
                        veiculo=veiculo,
                        status=status_enum
                    )
                    locacoes.append(loc)
            return locacoes
        except Exception as e:
            print("Erro ao buscar locações:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, locacao_id: int):
        if not self.conexao:
            return None
        try:
            cursor = self.conexao.cursor()
            query = "SELECT id, data_inicio, data_fim, veiculo_placa, status, valor_total FROM tb_locacoes WHERE id = %s"
            cursor.execute(query, (locacao_id,))
            linha = cursor.fetchone()
            if linha:
                veiculo = self.veiculo_dao.buscar_por_placa(linha[3])
                if veiculo:
                    status_enum = StatusLocacao(linha[4])
                    loc = locacao(
                        id=linha[0],
                        data_inicio=linha[1],
                        data_fim=linha[2],
                        veiculo=veiculo,
                        status=status_enum
                    )
                    return loc
            return None
        except Exception as e:
            print(f"Erro ao buscar locação {locacao_id}: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, locacao_obj: locacao):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE tb_locacoes 
                       SET data_inicio = %s, data_fim = %s, veiculo_placa = %s, status = %s, valor_total = %s 
                       WHERE id = %s"""
                       
            valor_total = None
            if locacao_obj.status == StatusLocacao.DEVOLVIDO:
                valor_total = locacao_obj.calcular_valor_locacao()
                
            cursor.execute(query, (
                locacao_obj.data_inicio,
                locacao_obj.data_fim,
                locacao_obj.veiculo.placa,
                locacao_obj.status.value,
                valor_total,
                locacao_obj.id
            ))
            self.conexao.commit()
            return True, "Locação atualizada com sucesso"
        except Exception as e:
            print(f"Erro ao atualizar locação {locacao_obj.id}: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar locação: {e}"
        finally:
            if cursor:
                cursor.close()

    def remover(self, locacao_id: int):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM tb_locacoes WHERE id = %s"
            cursor.execute(query, (locacao_id,))
            self.conexao.commit()
            return True, "Locação removida com sucesso"
        except Exception as e:
            print(f"Erro ao remover locação {locacao_id}: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover locação: {e}"
        finally:
            if cursor:
                cursor.close()

    def buscar_veiculos_disponiveis(self, data_inicio: date, data_fim: date, categoria_veiculo):
        if not self.conexao:
            return []
        try:
            cursor = self.conexao.cursor()
            # Veículos da categoria que NÃO possuem locações ativas (reservado ou locado)
            # interceptando o período [data_inicio, data_fim]
            query = """
                SELECT v.vei_placa 
                FROM veiculo v
                WHERE v.vei_categoria = %s 
                AND NOT EXISTS (
                    SELECT 1 FROM tb_locacoes l
                    WHERE l.veiculo_placa = v.vei_placa
                    AND l.status IN ('reservado', 'locado')
                    AND (l.data_inicio <= %s AND l.data_fim >= %s)
                )
            """
            cursor.execute(query, (categoria_veiculo.value, data_fim, data_inicio))
            linhas = cursor.fetchall()
            
            veiculos_disponiveis = []
            for linha in linhas:
                veiculo = self.veiculo_dao.buscar_por_placa(linha[0])
                if veiculo:
                    veiculos_disponiveis.append(veiculo)
                    
            return veiculos_disponiveis
        except Exception as e:
            print(f"Erro ao buscar veículos disponíveis: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
