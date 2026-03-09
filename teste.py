from model.veiculo_factory import VeiculoFactory
from model.locacao import locacao
from model.categoria import categoria
from datetime import date

print("\n[ TESTE 1 ]: Criação via Factory")
meu_carro = VeiculoFactory.criar_veiculo("carro", "ABC1234", categoria.ECONOMICO, 100)
meu_motorhome = VeiculoFactory.criar_veiculo("motorhome", "XYZ9876", categoria.EXECUTIVO, 350)
print(f"SUCESSO: Veículo '{type(meu_carro).__name__}' criado via Factory.")
print(f"SUCESSO: Veículo '{type(meu_motorhome).__name__}' criado via Factory.")

print("\n[ TESTE 2 ]: Cálculo com múltiplos dias")
locacao_longa = locacao(data_inicio=date(2023, 10, 1), data_fim=date(2023, 10, 5), veiculo=meu_carro)
valor = locacao_longa.calcular_valor_locacao()
print(f"Valor total da locação (4 dias): R$ {valor:.2f} (Esperado: R$ 450.00)")

print("\n[ TESTE 3 ]: Cálculo com devolução no mesmo dia")
locacao_curta = locacao(data_inicio=date(2023, 10, 1), data_fim=date(2023, 10, 1), veiculo=meu_motorhome)
valor = locacao_curta.calcular_valor_locacao()
print(f"Valor total da locação (Mesmo dia): R$ {valor:.2f} (Esperado: R$ 470.00)")

print("\n[ TESTE 4 ]: Tratamento de tipo inválido na fábrica")
try:
    VeiculoFactory.criar_veiculo("barco", "DEF1234", categoria.EXECUTIVO, 200)
except ValueError as e:
    print(f"SUCESSO: O sistema bloqueou a criação e gerou o erro -> {e}")