from model.veiculo_factory import VeiculoFactory
from model.locacao import locacao
from model.categoria import categoria
from model.decoradores import GPSDecorator, SeguroTerceirosDecorator
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

    print("\n--- TESTANDO O PADRÃO STATE RESTRITIVO ---")
carro_estado = VeiculoFactory.criar_veiculo("carro", "HJI3K45", categoria.ECONOMICO, 100.0)

carro_estado.tentar_alugar() 


carro_estado.tentar_alugar() 


carro_estado.reter_na_frota_pra_conserto() 


carro_estado.tentar_devolver() 


carro_estado.reter_na_frota_pra_conserto() 
carro_estado.tentar_alugar()



print("\n--- TESTANDO O PADRÃO DECORATOR ---")
locacao_base = locacao(data_inicio=date(2026, 3, 1), data_fim=date(2026, 3, 5), veiculo=meu_carro)
print(f"Valor Base (somente Diária + Seguro Base): R$ {locacao_base.calcular_valor_locacao()}")

locacao_com_gps = GPSDecorator(locacao_base)
print(f"Valor somado do pacote + GPS: R$ {locacao_com_gps.calcular_valor_locacao()}")

locacao_vip_top = SeguroTerceirosDecorator(locacao_com_gps)
print(f"Valor pacote completão (Base + GPS + Seg.Terceiros): R$ {locacao_vip_top.calcular_valor_locacao()}")