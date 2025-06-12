# API de Gerenciamento - Panificadora Trigão

Backend desenvolvido em FastAPI para o sistema de gerenciamento da Panificadora Trigão. A API oferece funcionalidades para controle de produtos e usuários, com uma arquitetura escalável e conectada a um banco de dados PostgreSQL.

## Principais Funcionalidades

-   ✅ **CRUD de Produtos**: Crie, leia, atualize e delete produtos do inventário.
-   ✅ **CRUD de Usuários**: Gerenciamento de usuários do sistema (funcionários, administradores).
-   ✅ **Banco de Dados Relacional**: Persistência de dados utilizando PostgreSQL com SQLAlchemy.
-   ✅ **Validação de Dados**: Uso de Pydantic para garantir a integridade dos dados de entrada e saída.
-   ✅ **Documentação Automática**: Interface interativa (Swagger UI e ReDoc) gerada automaticamente pelo FastAPI.

## Tecnologias Utilizadas

-   **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Banco de Dados**: [PostgreSQL](https://www.postgresql.org/)
-   **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
-   **Validação**: [Pydantic](https://docs.pydantic.dev/)
-   **Servidor ASGI**: [Uvicorn](https://www.uvicorn.org/)
-   **Segurança de Senhas**: [Passlib](https://passlib.readthedocs.io/en/stable/)
-   **Variáveis de Ambiente**: [Python-dotenv](https://pypi.org/project/python-dotenv/)

## Como Executar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em seu ambiente local.

### 1. Pré-requisitos

-   Python 3.10+
-   PostgreSQL instalado e rodando.
-   Git

### 2. Configuração do Ambiente

**a. Clone o repositório:**

```bash
git clone [https://github.com/caiorocha7/trigao-gerenciamento.git](https://github.com/caiorocha7/trigao-gerenciamento.git)
cd trigao-gerenciamento
```

**b. Crie e ative um ambiente virtual:**

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

**c. Instale as dependências:**

```bash
pip install -r requirements.txt
```

**d. Configure as variáveis de ambiente:**

Crie um arquivo chamado `.env` na raiz do projeto, copiando o exemplo abaixo. **Substitua os valores com suas credenciais do PostgreSQL.**

```env
# .env
DATABASE_URL="postgresql://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO"

# Exemplo para um banco de dados local:
# DATABASE_URL="postgresql://postgres:123456@localhost:5432/trigao_fastapi"
```

### 3. Executando a API

Com o ambiente virtual ativado e o arquivo `.env` configurado, inicie o servidor:

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

### 4. Acessando a Documentação

Para ver e interagir com todos os endpoints, acesse a documentação automática gerada pelo FastAPI:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

## Populando o Banco de Dados

Para carregar os dados iniciais dos produtos, utilize o script `populate_db.py`. Certifique-se de que o arquivo `produtos-trigao.json` está na raiz do projeto.

Com a API rodando, abra um **novo terminal** e execute:

```bash
python populate_db.py
```

## Próximos Passos

-   [ ] Implementar autenticação de usuários com JWT.
-   [ ] Proteger os endpoints de modificação de dados.
-   [ ] Adicionar filtros avançados de busca para produtos (nome, preço, seção).
-   [ ] Criar um endpoint para listar as seções de produtos.