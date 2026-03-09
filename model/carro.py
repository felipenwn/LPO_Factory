from model.veiculo import veiculo
class carro(veiculo):
    def __init__(self, placa, categoria, taxa_diaria):
        super().__init__(placa, taxa_diaria, categoria)
        self.__valor_do_seguro = 50

    @property   
    def valor_do_seguro(self):
        return self.__valor_do_seguro
    
    @valor_do_seguro.setter
    def valor_do_seguro(self,valor_do_seguro):
       self.__valor_do_seguro = valor_do_seguro
