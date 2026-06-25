from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import motor, Base, SessaoLocal
from domain import modelos
from application import schemas
from infrastructure.seguranca import gerar_hash_senha
from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

# Configurações de Segurança JWT
SECRET_KEY = "super_segredo_raizes_do_nordeste_que_ninguem_pode_saber"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Configuração do verificador de senhas (desembaralhador)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cria as tabelas no banco de dados (se ainda não existirem)
Base.metadata.create_all(bind=motor)

app = FastAPI(
    title="API Raízes do Nordeste",
    description="Sistema multicanal para controle de pedidos e estoque",
    version="1.0.0"
)

# Dependência: Abre uma "sessão" com o banco de dados e fecha ao terminar
def obter_banco():
    banco = SessaoLocal()
    try:
        yield banco
    finally:
        banco.close()

# Rota para cadastrar um novo usuário
@app.post("/usuarios/", response_model=schemas.UsuarioResposta, status_code=201)
def criar_usuario(usuario: schemas.UsuarioCriar, banco: Session = Depends(obter_banco)):
    
    # 1. Verifica se o e-mail já está cadastrado no banco de dados
    usuario_existente = banco.query(modelos.Usuario).filter(modelos.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # 2. Criptografa a senha recebida
    senha_criptografada = gerar_hash_senha(usuario.senha)

    # 3. Monta o objeto do usuário para salvar no banco (sem a senha pura)
    novo_usuario = modelos.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_criptografada,
        consentimento_lgpd=usuario.consentimento_lgpd
    )

    # 4. Salva efetivamente no banco de dados SQLite
    banco.add(novo_usuario)
    banco.commit()
    banco.refresh(novo_usuario)

    # Retorna o usuário criado (o Pydantic vai filtrar e esconder a senha_hash automaticamente)
    return novo_usuario

# Rota para cadastrar uma nova unidade (filial)
@app.post("/unidades/", response_model=schemas.UnidadeResposta, status_code=201)
def criar_unidade(unidade: schemas.UnidadeCriar, banco: Session = Depends(obter_banco)):
    
    # Cria a instância do modelo com os dados validados
    nova_unidade = modelos.Unidade(
        nome=unidade.nome,
        endereco=unidade.endereco
    )

    # Registra no banco de dados
    banco.add(nova_unidade)
    banco.commit()
    banco.refresh(nova_unidade)

    # Retorna os dados com o ID gerado
    return nova_unidade

# --- ROTAS DE PRODUTOS ---

@app.post("/produtos/", response_model=schemas.ProdutoResposta, status_code=201)
def criar_produto(produto: schemas.ProdutoCriar, banco: Session = Depends(obter_banco)):
    novo_produto = modelos.Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco
    )
    banco.add(novo_produto)
    banco.commit()
    banco.refresh(novo_produto)
    return novo_produto


# --- ROTAS DE ESTOQUE ---

@app.post("/estoques/", response_model=schemas.EstoqueResposta, status_code=201)
def criar_estoque(estoque: schemas.EstoqueCriar, banco: Session = Depends(obter_banco)):
    novo_estoque = modelos.Estoque(
        unidade_id=estoque.unidade_id,
        produto_id=estoque.produto_id,
        quantidade=estoque.quantidade
    )
    banco.add(novo_estoque)
    banco.commit()
    banco.refresh(novo_estoque)
    return novo_estoque

# --- ROTAS DE PEDIDOS ---

@app.post("/pedidos/", response_model=schemas.PedidoResposta, status_code=201)
def criar_pedido(pedido: schemas.PedidoCriar, banco: Session = Depends(obter_banco), token: str = Depends(oauth2_scheme)):
    
    # 1. Cria a "capa" do pedido
    novo_pedido = modelos.Pedido(
        usuario_id=pedido.usuario_id,
        unidade_id=pedido.unidade_id,
        canal_pedido=pedido.canal_pedido,
        forma_pagamento=pedido.forma_pagamento
    )
    banco.add(novo_pedido)
    banco.flush() # Reserva o ID do pedido no banco antes de salvar definitivamente
    
    total_pedido = 0.0
    
    # 2. Processa cada produto da lista do cliente
    for item in pedido.itens:
        # Verifica se o produto existe e pega o preço real dele no banco
        produto_db = banco.query(modelos.Produto).filter(modelos.Produto.id == item.produto_id).first()
        
        if not produto_db:
            raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id} não encontrado no cardápio")
        
        # Cria a linha do item conectando ao pedido
        novo_item = modelos.ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=produto_db.preco
        )
        banco.add(novo_item)
        
        # Multiplica a quantidade pelo preço e soma no total da nota
        total_pedido += (produto_db.preco * item.quantidade)
        
    # 3. Grava o valor total calculado e finaliza a transação
    novo_pedido.total = total_pedido
    banco.commit()
    banco.refresh(novo_pedido)
    
    return novo_pedido

# --- ROTA DE AUTENTICAÇÃO (LOGIN) ---

@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), banco: Session = Depends(obter_banco)):
    # Procura o utilizador pelo e-mail (o FastAPI usa o campo 'username' para o login padrão)
    usuario_db = banco.query(modelos.Usuario).filter(modelos.Usuario.email == form_data.username).first()
    
    # Valida se o utilizador existe e compara a senha digitada com o Hash do banco
    if not usuario_db or not pwd_context.verify(form_data.password, usuario_db.senha_hash):
        raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
    
    # Se os dados estiverem corretos, gera o Token JWT
    tempo_expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_token = {"sub": usuario_db.email, "exp": tempo_expiracao}
    token_jwt = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token_jwt, "token_type": "bearer"}
