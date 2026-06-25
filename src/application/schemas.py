from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from domain.modelos import CanalPedidoEnum

# Molde para receber os dados quando alguém se cadastrar
class UsuarioCriar(BaseModel):
    nome: str
    email: EmailStr
    senha: str  # A senha chega pura aqui, mas vou criptografar antes de salvar no banco
    consentimento_lgpd: bool = False  # Atendendo ao requisito da LGPD do projeto

# Molde para devolver os dados pra tela (nunca devolver a senha!)
class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str

    # Configuração necessária pro FastAPI entender os dados que vêm do banco de dados
    class Config:
        from_attributes = True

# Filtro para os dados de entrada na criacao de uma nova filial
class UnidadeCriar(BaseModel):
    nome: str
    endereco: str

# Filtro para a devolucao dos dados da filial
class UnidadeResposta(BaseModel):
    id: int
    nome: str
    endereco: str

    class Config:
        from_attributes = True


# --- ESQUEMAS DE PRODUTO ---
class ProdutoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float

class ProdutoCriar(ProdutoBase):
    pass

class ProdutoResposta(ProdutoBase):
    id: int

    class Config:
        from_attributes = True  # Permite que o Pydantic leia modelos do SQLAlchemy


# --- ESQUEMAS DE ESTOQUE ---
class EstoqueBase(BaseModel):
    unidade_id: int
    produto_id: int
    quantidade: int

class EstoqueCriar(EstoqueBase):
    pass

class EstoqueResposta(EstoqueBase):
    id: int

    class Config:
        from_attributes = True

# --- ESQUEMAS DE ITEM DO PEDIDO ---
class ItemPedidoBase(BaseModel):
    produto_id: int
    quantidade: int

class ItemPedidoCriar(ItemPedidoBase):
    pass

class ItemPedidoResposta(ItemPedidoBase):
    id: int
    preco_unitario: float

    class Config:
        from_attributes = True


# --- ESQUEMAS DE PEDIDO ---
class PedidoBase(BaseModel):
    usuario_id: int
    unidade_id: int
    canal_pedido: CanalPedidoEnum
    forma_pagamento: str

class PedidoCriar(PedidoBase):
    # Uma lista permitindo que um pedido tenha vários itens diferentes
    itens: List[ItemPedidoCriar]

class PedidoResposta(PedidoBase):
    id: int
    status: str
    total: float
    data_criacao: datetime
    # Retorna o pedido já com os detalhes dos itens comprados
    itens: List[ItemPedidoResposta]

    class Config:
        from_attributes = True