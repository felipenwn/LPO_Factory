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
                database = "lpo_factory"
            )
            return conexao
        except Error as e:
            print("Erro ao conectar ao banco de dados:", e)
            return None

    @staticmethod
    def setup_database():
        conexao = DatabaseConfig.get_connection()
        if conexao:
            try:
                cursor = conexao.cursor()
                # Tabela de Veículos (já existente, mas garantimos a estrutura)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS veiculo (
                        vei_placa VARCHAR(7) PRIMARY KEY,
                        vei_categoria VARCHAR(50) NOT NULL,
                        vei_taxa_diaria DECIMAL(10,2) NOT NULL,
                        vei_estado_atual VARCHAR(50),
                        vei_tipo VARCHAR(50) NOT NULL
                    )
                """)
                # Tabela de Locações
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tb_locacoes (
                        id SERIAL PRIMARY KEY,
                        data_inicio DATE NOT NULL,
                        data_fim DATE NOT NULL,
                        veiculo_placa VARCHAR(7) NOT NULL,
                        status VARCHAR(20) NOT NULL,
                        valor_total DECIMAL(10,2),
                        FOREIGN KEY (veiculo_placa) REFERENCES veiculo(vei_placa)
                    )
                """)
                conexao.commit()
                print("Tabelas verificadas/criadas com sucesso.")
            except Error as e:
                print("Erro ao criar as tabelas:", e)
                conexao.rollback()
            finally:
                if cursor:
                    cursor.close()
                conexao.close()