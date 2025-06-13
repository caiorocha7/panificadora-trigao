from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from . import models, crud, schemas
from .database import SessionLocal, engine
from .routers import auth as auth_router, products as products_router, orders as orders_router

# Cria as tabelas no banco de dados, se não existirem
models.Base.metadata.create_all(bind=engine)

# --- Nova função de ciclo de vida (lifespan) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização da aplicação
    print("Iniciando a aplicação...")
    db = SessionLocal()
    try:
        admin_user = crud.get_user_by_username(db, username="admin")
        if not admin_user:
            print("Criando usuário ADMIN padrão...")
            user_in = schemas.UserCreate(
                username="admin",
                email="admin@trigao.com",
                password="123456"  # Em produção, use variável de ambiente
            )
            crud.create_user(db=db, user=user_in, role=schemas.Role.ADMIN)
            print("Usuário ADMIN criado com sucesso.")
    finally:
        db.close()

    yield  # A aplicação roda aqui

    # Encerramento da aplicação (opcional)
    print("Finalizando a aplicação...")

# Cria a instância do FastAPI com a função de ciclo de vida
app = FastAPI(title="Panificadora Trigão API", lifespan=lifespan)

# --- Configuração do CORS ---
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# --- Inclusão dos Roteadores ---
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(orders_router.router)

# --- Rota raiz ---
@app.get("/")
def root():
    return {"message": "Bem-vindo à API da Panificadora Trigão"}
