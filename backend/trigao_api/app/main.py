from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, crud, schemas
from .database import SessionLocal, engine
from .routers import auth as auth_router, products as products_router

# Cria as tabelas no banco de dados, se não existirem
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Panificadora Trigão API")

# --- Configuração do CORS ---
origins = [
    "http://localhost:5173",  # Endereço do frontend React/Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# --- Evento de Startup para criar usuário Admin ---
@app.on_event("startup")
def on_startup():
    db = SessionLocal()
    try:
        # Verifica se o usuário admin já existe
        admin_user = crud.get_user_by_username(db, username="admin")
        if not admin_user:
            # Cria o usuário admin se ele não existir
            print("Criando usuário ADMIN padrão...")
            user_in = schemas.UserCreate(
                username="admin",
                email="admin@trigao.com",
                password="123456" # Use uma senha forte e mova para variáveis de ambiente em produção
            )
            crud.create_user(db=db, user=user_in, role=schemas.Role.ADMIN)
            print("Usuário ADMIN criado com sucesso.")
    finally:
        db.close()

# --- Inclusão dos Roteadores ---
app.include_router(auth_router.router)
app.include_router(products_router.router)
# ... inclua outros roteadores aqui no futuro

@app.get("/")
def root():
    return {"message": "Bem-vindo à API da Panificadora Trigão"}