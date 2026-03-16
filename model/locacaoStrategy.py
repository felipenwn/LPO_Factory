from abc import ABC, abstractmethod
from .veiculo import veiculo
class CalculoLocacaoStrategy(ABC):
    @abstractmethod
    def calcular_diarias(self, veiculo:veiculo,dias:int)->float:
        pass

class CalculoPadraoStrategy(CalculoLocacaoStrategy):
    def calcular_diarias(self, veiculo:veiculo, dias:int)->float:
        valor_diarias = veiculo.taxa_diaria * dias
        return(valor_diarias + veiculo.valor_do_seguro)

class CalculoVIPStrategy(CalculoLocacaoStrategy):
    def calcular_diarias(self, veiculo:veiculo, dias:int)->float:
        valor_diarias = veiculo.taxa_diaria * dias
        return((valor_diarias * 0.8)+ veiculo.valor_do_seguro) 