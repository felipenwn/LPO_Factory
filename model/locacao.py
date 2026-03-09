from model.veiculo import veiculo
from datetime import date
from model.exception import DataInvalidaError

class locacao:
    def __init__(self, data_inicio:date, data_fim:date, veiculo:veiculo):
        if data_fim < data_inicio:
            raise DataInvalidaError("A data de devolução não pode ser anterior à data de início.")
        
        self.__data_inicio = data_inicio
        self.__data_fim = data_fim
        self.veiculo = veiculo

    def calcular_valor_locacao(self):
            delta = self.__data_fim - self.__data_inicio
            dias = delta.days
            if dias <= 0:
                 dias = 1
            valor_diarias = dias * self.veiculo.taxa_diaria
            valor_total = valor_diarias + self.veiculo.valor_do_seguro
        
            return valor_total
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