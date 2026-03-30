from abc import ABC, abstractmethod

class GenericDAO(ABC):
    @abstractmethod
    def salvar(self, objeto):
        pass

    @abstractmethod
    def listar_todos(self):
        pass

    @abstractmethod
    def atualizar(self, objeto):
        pass

    @abstractmethod
    def remover(self, id):
        pass