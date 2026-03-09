from model.veiculo_factory import VeiculoFactory
from model.locacao import locacao
from model.categoria import categoria
from datetime import date

meu_carro = VeiculoFactory.criar_veiculo("carro", "ABC1234", categoria.ECONOMICO, 100)
meu_motorhome = VeiculoFactory.criar_veiculo("motorhome", "XYZ9876", categoria.EXECUTIVO, 350)

data_inicio = date(2023, 10, 1)
data_fim = date(2023, 10, 5)

locacao_1 = locacao(veiculo=meu_carro, data_inicio=data_inicio, data_fim=data_fim)
locacao_2 = locacao(veiculo=meu_motorhome, data_inicio=data_inicio, data_fim=data_fim)

print(f"O veículo alugado 1 é da categoria {locacao_1.veiculo.categoria.value} e paga R${locacao_1.veiculo.valor_do_seguro} de seguro.")
print(f"O valor total da locação 1 (4 dias) é: R$ {locacao_1.calcular_valor_locacao()}")

print("-" * 30)

print(f"O veículo alugado 2 é da categoria {locacao_2.veiculo.categoria.value} e paga R${locacao_2.veiculo.valor_do_seguro} de seguro.")
print(f"O valor total da locação 2 (4 dias) é: R$ {locacao_2.calcular_valor_locacao()}")