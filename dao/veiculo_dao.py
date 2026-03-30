import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from LPO_Factory.model.veiculo_factory import VeiculoFactory
from generic_dao import GenericDAO
from dao.db_config import DatabaseConfig
from model.veiculo import *

class VeiculoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()
    def salvar(self, veiculo):
        if not self.conexao:
            raise Exception("Não foi possível conectar ao banco de dados.")
        try:
            cursor = self.conexao.cursor()
            query = "INSERT INTO veiculo (vei_placa, vei_categoria, vei_taxa_diaria,vei_estado_atual, vei_tipo) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (veiculo.placa, veiculo.categoria.value, veiculo.taxa_diaria, veiculo.estado_atual.__class__.__name__(), veiculo.tipo))
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
            query = "SELECT vei_tipo, vei_placa, vei_categoria, vei_taxa_diaria FROM tb_veiculos"
            linhas = cursor.fetchall()
            veiculos = []
            for cada_linha in linhas:
                obj = VeiculoFactory.criar_veiculo(cada_linha[0],cada_linha[1],cada_linha[2],float(cada_linha[3]))
                veiculos.append(obj)
            return veiculos
        except Exception as e:
            print("Erro ao buscar veículos:", e)
            return []
        finally:
            if cursor:
                cursor.close()

