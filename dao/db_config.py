import psycopg2
from psycopg2 import Error

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                user = "pgadmin",
                password = "pgadmin",
                host = "localhost",
                port = "5432",
                database = "lpo_factory"
            )
        except Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None