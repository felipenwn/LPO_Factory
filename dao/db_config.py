import psycopg2
from psycopg2 import Error

class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            conexao = psycopg2.connect(
                user = "postgres",
                password = "postgres",
                host = "localhost",
                port = "5432",
                database = "db_lpoo_locadora_veic"
            )
            return conexao
        except Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None