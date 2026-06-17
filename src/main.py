
from fastapi import FastAPI

# Iniciando o sistema da lanchonete
app = FastAPI(
    title="API Raízes do Nordeste",
    description="Sistema multicanal para controle de pedidos e estoque",
    version="1.0.0"
)

# Rota inicial só para testar se o servidor está funcionando
@app.get("/")
def teste_servidor():
    return {"mensagem": "API Raizes do Nordeste rodando com sucesso!"}
