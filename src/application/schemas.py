from pydantic import BaseModel, EmailStr

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
        