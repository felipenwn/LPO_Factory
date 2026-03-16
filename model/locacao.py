from model.veiculo import veiculo
from datetime import date
from model.exception import DataInvalidaError

class locacao:
    def __init__(self, data_inicio:date, data_fim:date, veiculo:veiculo):
        if data_fim < data_inicio:
            raise DataInvalidaError("A data de devolução não pode ser anterior à data de início.")
        
        self.data_inicio = data_inicio
        self.data_fim = date.today()
        self.veiculo = veiculo

    def calcular_valor_locacao(self):
            if self.data_fim is None:
                self.data_fim = date.today()
            dias = (self.data_fim - self.data_inicio).days
            if dias <= 0:
                 dias = 1
            valor_total = self.estrategia.calcular_diarias(self.veiculo, dias)
            return float(valor_total)
    @property   
    def veiculo(self):
        return self.__veiculo
    
    @veiculo.setter
    def veiculo(self,obj):
        if(obj is not None):
            self.__veiculo = obj
        else:
            raise Exception("Objeto Veículo obrigatório !!")
        
    

    @property   
    def placa(self):
        return self.__placa            