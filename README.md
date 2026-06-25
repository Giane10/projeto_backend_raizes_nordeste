# 🌵 API Raízes do Nordeste

Bem-vindo ao repositório da API do **Raízes do Nordeste**, um sistema multicanal para controle de pedidos e estoque, desenvolvido como MVP (Produto Mínimo Viável) acadêmico. 

Este projeto foi construído com foco em boas práticas de mercado, adotando a mentalidade **DevSecOps (Shift-Left)** para garantir a segurança desde a primeira linha de código, além de seguir os princípios da LGPD.

## 🛠️ Tecnologias Utilizadas
* **Python 3**
* **FastAPI** (Framework web ágil e moderno)
* **SQLite** (Banco de dados leve e integrado)
* **SQLAlchemy** (ORM para mapeamento das tabelas)
* **Pydantic** (Validação rigorosa de dados)
* **Bcrypt & JWT** (Criptografia e autenticação segura)

## 🎯 Progresso do Projeto (Roadmap)
Aqui está o nosso mapa de desenvolvimento. As etapas marcadas com 'x' já estão prontas e rodando no laboratório!

- [x] 1. Criar estrutura de pastas e ambiente virtual
- [x] 2. Configurar segurança inicial (Cofres `.env` e `.gitignore` oficial)
- [x] 3. Estabelecer conexão com o Banco de Dados
- [x] 4. Criar Entidade e Rota de Cadastro de **Usuário** (com hash de senha)
- [x] 5. Criar Entidade de **Unidade** (Filial)
- [x] 6. Criar Entidades de **Produto** e **Estoque**
- [x] 7. Criar Entidade e Lógica de **Pedido**
- [x] 8. Implementar sistema de **Login com Token JWT**
- [ ] 9. Finalizar rotas de listagem de cardápio e checkout

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3
* Git

### Passo a Passo

1. **Clone o repositório e entre na pasta:**
    ```bash
   git clone [https://github.com/Giane10/projeto_backend_raizes_nordeste.git](https://github.com/Giane10/projeto_backend_raizes_nordeste.git)

   cd projeto_backend_raizes_nordeste
    ```
2. **Crie e ative o ambiente virtual:**
    ```bash
    python -m venv venv

    source venv/Scripts/activate  # (No Windows via Git Bash)
    ```
3. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configuração de Segurança:**
    * Crie um arquivo .env na raiz do projeto (use o .env.example como base) para guardar suas credenciais.

5. **Inicie o servidor da API:**
    ```bash
    cd src
    
    uvicorn main:app --reload
    ```
6. **Acesse o Painel de Testes (Swagger UI):**
    
    * Abra o navegador no endereço: http://127.0.0.1:8000/docs
    

---

## 🛡️ Diferenciais e Boas Práticas (Segurança e Qualidade)

Além dos requisitos solicitados, este projeto foi desenvolvido com foco na qualidade contínua e segurança do código. Para isso, foi utilizado o **SonarQube/SonarLint** integrado ao ambiente de desenvolvimento como ferramenta de análise estática (SAST). 

Essa prática garantiu:
* **Aderência ao Clean Code:** Identificação e correção em tempo real de *code smells* e práticas obsoletas.
* **Segurança Proativa:** Mitigação de potenciais vulnerabilidades na manipulação de dados sensíveis e fusos horários (adoção rigorosa do padrão UTC).
* **Desenvolvimento Sustentável:** Manutenção de um código limpo, padronizado e pronto para escalar com segurança.

--- 

*Desenvolvido por Giane Costa*