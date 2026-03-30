import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.db_config import DatabaseConfig

if DatabaseConfig.get_connection():
    print("Conexão bem-sucedida!")  
else:
    print("Falha na conexão com o banco de dados.")