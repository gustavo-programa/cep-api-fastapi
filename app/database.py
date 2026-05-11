from sqlalchemy import create_engine # Ferramenta para conectar ao banco
from sqlalchemy.ext.declarative import declarative_base # Classe base para os modelos
from sqlalchemy.orm import sessionmaker # Ferramenta para criar sessões de conversa com o banco

# A "ponte" para o seu MySQL. Mude 'suasenha' para a senha do seu root!
# O final '/cep_db' indica que vamos usar o novo banco que você criou.
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/cep_db"

# Cria o motor de conexão
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões (cada busca no banco é uma sessão nova)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe que usaremos no models.py para criar as tabelas
Base = declarative_base()

# Função auxiliar para abrir e fechar a conexão automaticamente
def get_db():
    db = SessionLocal() # Abre a conexão
    try:
        yield db # Entrega a conexão para quem pediu
    finally:
        db.close() # Fecha a conexão ao terminar a tarefa