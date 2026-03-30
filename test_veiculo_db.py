import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from LPO_Factory.model.veiculo_factory import VeiculoFactory
from model.veiculo import *
from dao.veiculo_dao import VeiculoDAO
dao = VeiculoDAO()
novo_carro = VeiculoFactory.criar_veiculo("carro", "ABC1D34", categoria.ECONOMICO, 150.00)
dao.salvar(novo_carro)

lista_veiculos = dao.listar_todos()

print("\nVeículos cadastrados no banco de dados:")
for obj in lista_veiculos:
    print(obj)
