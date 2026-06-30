from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from infrastructure.database import Base
import enum
from datetime import datetime

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
    
    # salvamos apenas o hash irreversível
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
      
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    
    # O relacionamento ligando o produto ao estoque
    estoques = relationship("Estoque", back_populates="produto")


class Estoque(Base):
    __tablename__ = "estoques"

    id = Column(Integer, primary_key=True, index=True)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, default=0, nullable=False)

    # Relacionamentos para o banco entender as ligações
    produto = relationship("Produto", back_populates="estoques")
    unidade = relationship("Unidade")

# Definição do ENUM para multicanalidade
class CanalPedidoEnum(str, enum.Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    unidade_id = Column(Integer, ForeignKey("unidades.id"), nullable=False)
    
    # Campo obrigatório de multicanalidade
    canal_pedido = Column(Enum(CanalPedidoEnum), nullable=False)
    
    status = Column(String, default="AGUARDANDO_PAGAMENTO", nullable=False)
    total = Column(Float, default=0.0, nullable=False)
    forma_pagamento = Column(String, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamentos para o ORM orquestrar os dados
    usuario = relationship("Usuario")
    unidade = relationship("Unidade")
    itens = relationship("ItemPedido", back_populates="pedido")


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    # Ligações reversas
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")

