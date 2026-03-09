from model.carro import carro
from model.motorhome import motorhome

class VeiculoFactory:
    @staticmethod
    def criar_veiculo(tipo: str, placa: str, categoria, taxa_diaria: float):
        tipo = tipo.strip().lower() 
        
        if taxa_diaria <= 0:
            raise ValueError("A taxa diária deve ser um valor positivo e maior que zero.")
         
        if tipo == "carro":
            return carro(placa, categoria, taxa_diaria)
        elif tipo == "motorhome":
            return motorhome(placa, categoria, taxa_diaria)
        else:
            raise ValueError(f"Tipo de veículo '{tipo}' não é fabricado por esta fábrica.")