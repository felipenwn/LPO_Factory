from views.main_window import iniciar_aplicacao
from dao.db_config import DatabaseConfig

if __name__ == "__main__":
    DatabaseConfig.setup_database()
    iniciar_aplicacao()