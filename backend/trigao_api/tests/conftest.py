import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session 

from app import schemas

from app.main import app
from app.database import Base
from app.auth import get_db, create_access_token
from app.schemas import Role
from app import models, crud

# --- Configuração do Banco de Dados de Teste ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# --- Fixtures do Pytest ---

@pytest.fixture(scope="function")
def db_session():
    """Cria uma nova sessão de banco de dados para cada teste e limpa depois."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# 👇 MUDANÇA AQUI 👇
@pytest.fixture(scope="function")
def client(db_session):
    """Cria um cliente de teste para a API, usando o banco de dados de teste."""
    def override_get_db():
        # Usar db_session aqui dentro, que é recriada para cada teste
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

# 👇 MUDANÇA AQUI 👇
@pytest.fixture(scope="function")
def admin_auth_headers(client: TestClient, db_session: Session):
    """Cria um usuário ADMIN e retorna cabeçalhos de autenticação para ele."""
    user = crud.create_user(db_session, schemas.UserCreate(username="testadmin", email="admin@test.com", password="password"), role=Role.ADMIN)
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"Authorization": f"Bearer {token}"}

# 👇 MUDANÇA AQUI 👇
@pytest.fixture(scope="function")
def normal_user_auth_headers(client: TestClient, db_session: Session):
    """Cria um usuário USER e retorna cabeçalhos de autenticação para ele."""
    user = crud.create_user(db_session, schemas.UserCreate(username="testuser", email="user@test.com", password="password"), role=Role.USER)
    token = create_access_token(data={"sub": user.username, "role": user.role})
    return {"Authorization": f"Bearer {token}"}