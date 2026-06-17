from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. O endereço do banco SQLite 
URL_DO_BANCO = "sqlite:///./raizes.db"

# 2. O motor que faz a conexão
motor = create_engine(
    URL_DO_BANCO, connect_args={"check_same_thread": False}
)

# 3. A sessão (o túnel de comunicação com o banco)
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor)

# 4. A base que vai transformar as classes Python em tabelas
Base = declarative_base()
