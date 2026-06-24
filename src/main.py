from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure.database import motor, Base, SessaoLocal
from domain import modelos
from application import schemas
from infrastructure.seguranca import gerar_hash_senha

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
