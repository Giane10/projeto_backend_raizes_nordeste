from fastapi import FastAPI
# Importei a conexão e a Base do banco
from infrastructure.database import motor, Base
# Importamos os modelos para que o SQLAlchemy saiba quais tabelas criar
from domain import modelos 

# Essa é a linha mágica! Ela diz: "Olhe para a Base, veja todos os modelos que 
# estão ligados a ela e crie as tabelas lá no nosso motor (SQLite)"
Base.metadata.create_all(bind=motor)

# Iniciando o sistema da lanchonete
app = FastAPI(
    title="API Raízes do Nordeste",
    description="Sistema multicanal para controle de pedidos e estoque",
    version="1.0.0"
)

# Rota inicial
@app.get("/")
def teste_servidor():
    return {"mensagem": "API Raizes do Nordeste rodando com sucesso!"}
