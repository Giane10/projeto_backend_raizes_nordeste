import bcrypt

# Função para embaralhar a senha e aplicar a regra de segurança do projeto
def gerar_hash_senha(senha: str) -> str:
    # O bcrypt pega a senha pura, joga um "sal" (dados aleatórios) e cria o hash irreversível
    sal = bcrypt.gensalt()
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), sal)
    
    # Devolvo o resultado como texto normal para conseguir salvar lá na tabela do SQLite
    return senha_criptografada.decode('utf-8')