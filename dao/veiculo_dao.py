import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.veiculo_factory import VeiculoFactory
from dao.generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from model.veiculo import *
from model.categoria import categoria

class VeiculoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
    def salvar(self, veiculo):
        if not self.conexao:
            raise Exception("Não foi possível conectar ao banco de dados.")
        try:
            cursor = self.conexao.cursor()
            query = "INSERT INTO veiculo (vei_placa, vei_categoria, vei_taxa_diaria,vei_estado_atual, vei_tipo) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (veiculo.placa, veiculo.categoria.value, veiculo.taxa_diaria, veiculo.estado_atual.__class__.__name__, type(veiculo).__name__))
            self.conexao.commit()
            return True,"Veículo salvo com sucesso."
        except Exception as e:
            print(f"Erro ao inserir veículo:{veiculo.placa}:", {e})
            self.conexao.rollback()
            return False,"Erro ao salvar veículo."
        finally:
            if cursor:
                cursor.close()
                
    def listar_todos(self):
        if not self.conexao:
            return []
        try:
            cursor = self.conexao.cursor()
            query = "SELECT vei_tipo, vei_placa, vei_categoria, vei_taxa_diaria FROM veiculo"
            cursor.execute(query)
            linhas = cursor.fetchall()
            veiculos = []
            for cada_linha in linhas:
                cat_enum = categoria(cada_linha[2])
                obj = VeiculoFactory.criar_veiculo(cada_linha[0],cada_linha[1],cat_enum,float(cada_linha[3]))
                veiculos.append(obj)
            return veiculos
        except Exception as e:
            print("Erro ao buscar veículos:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def buscar_por_placa(self, placa: str):
        if not self.conexao:
            return None
        try:
            cursor = self.conexao.cursor()
            query = "SELECT vei_tipo, vei_placa, vei_categoria, vei_taxa_diaria FROM veiculo WHERE vei_placa = %s"
            cursor.execute(query, (placa,))
            linha = cursor.fetchone()
            
            if linha: 
                cat_enum = categoria(linha[2])
                return VeiculoFactory.criar_veiculo(linha[0], linha[1], cat_enum, float(linha[3]))
            return None
        except Exception as e:
            print(f"Erro ao buscar veículo: {placa}. Erro: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def remover(self, placa: str):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        try:
            cursor = self.conexao.cursor()
            query = "DELETE FROM veiculo WHERE vei_placa = %s"
            cursor.execute(query, (placa,))
            self.conexao.commit()
            return True, "Veículo removido com sucesso"
        except Exception as e:
            print(f"Erro ao remover veículo: {placa}. Erro: {e}")
            self.conexao.rollback()
            return False, f"Erro ao remover veículo: {placa}: {e}"
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, veiculo):
        if not self.conexao:
            return False, "Sem conexão com o BD"
        try:
            cursor = self.conexao.cursor()
            query = """UPDATE veiculo 
                    SET vei_categoria = %s, vei_taxa_diaria = %s, vei_estado_atual = %s, vei_tipo = %s 
                    WHERE vei_placa = %s"""
            cursor.execute(query, (veiculo.categoria.value,
                                   veiculo.taxa_diaria,
                                   veiculo.estado_atual.__class__.__name__,
                                   type(veiculo).__name__,
                                   veiculo.placa))
            self.conexao.commit()
            return True, "Veículo atualizado com sucesso"
        except Exception as e:
            print(f"Erro ao atualizar veículo: {veiculo.placa}: {e}")
            self.conexao.rollback()
            return False, f"Erro ao atualizar veículo: {veiculo.placa}: {e}"
        finally:
            if cursor:
                cursor.close()
