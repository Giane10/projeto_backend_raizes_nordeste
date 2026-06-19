from sqlalchemy import Column, Integer, String, Boolean
# Importa a Base que criei na infraestrutura
from infrastructure.database import Base

class Usuario(Base):
    # Nome exato da tabela que será criada no banco de dados
    __tablename__ = "usuarios"

    # id (PK - Primary Key): Identificador único do usuário
    id = Column(Integer, primary_key=True, index=True)
    
    # Dados cadastrais básicos
    nome = Column(String, nullable=False)
    
    # email (Unique): Não podem existir dois usuários com o mesmo e-mail
    # o banco de dados não pode aceitar um usuário sem nome ou sem senha
    email = Column(String, unique=True, index=True, nullable=False)  
    
    # senha_hash: Regra de DevSecOps! Nunca salvamos a senha pura, apenas o hash irreversível
    senha_hash = Column(String, nullable=False)
    
    # perfil (Role): Controle de acesso (Ex: CLIENTE, ADMIN, COZINHA)
    perfil = Column(String, default="CLIENTE", nullable=False)
    
    # consentimento_lgpd: Booleano (Verdadeiro ou Falso) para registrar o aceite do usuário
    consentimento_lgpd = Column(Boolean, default=False)

class Unidade(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
      