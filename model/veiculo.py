from abc import ABC, abstractmethod
from .categoria import categoria
from .exception import PlacaInvalidaError, DataInvalidaError
from .estados_veiculo import DisponivelState 
class veiculo(ABC):
    def __init__(self, placa:str, taxa_diaria:float, categoria = categoria.ECONOMICO):
        self.__placa = placa
        self.categoria = categoria
        self.__taxa_diaria = taxa_diaria
        self.estado_atual = DisponivelState(self)
        
    @property   
    def placa(self):
        return self.__placa
    
    @property
    @abstractmethod
    def valor_do_seguro(self):
        pass
    
    @property   
    def taxa_diaria(self):
        return self.__taxa_diaria

    @taxa_diaria.setter
    def taxa_diaria(self,taxa_diaria):
        self.__taxa_diaria = taxa_diaria

    @placa.setter
    def placa(self,placa):
       placa = placa.strip().replace("-","").upper()
       if(len(placa) !=7):
              raise PlacaInvalidaError("Placa deve conter 7 caracteres")
       else:
           if not placa[0:3].isalpha():
               raise PlacaInvalidaError("Primeiros três caracteres devem ser letras")
           else:
               if not (placa[3].isdigit() and placa[5:7].isdigit()):
                   raise PlacaInvalidaError("Quarto caractere deve ser um número e os últimos dois caracteres devem ser números")
               elif not placa[4].isalpha():
                     raise PlacaInvalidaError("Quinto caractere deve ser uma letra")
               else:
                    print(f"placa {placa} é válida")

    @property
    def estado_atual(self):
        return self._estado_atual

    @estado_atual.setter
    def estado_atual(self, novo_estado):
        self._estado_atual = novo_estado
        
    def tentar_alugar(self):
        self.estado_atual.alugar()
        
    def tentar_devolver(self):
        self.estado_atual.devolver()
        
    def reter_na_frota_pra_conserto(self):
        self.estado_atual.enviar_manutencao()