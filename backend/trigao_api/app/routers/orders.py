from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas, auth

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
    dependencies=[Depends(auth.get_current_active_user)] # Protege todas as rotas deste router
)

@router.post("/", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_new_order(
    order_in: schemas.OrderCreate,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Cria um novo pedido para o usuário atualmente logado.
    Acessível por qualquer usuário autenticado.
    """
    try:
        return crud.create_order(db=db, order_in=order_in, user_id=current_user.id)
    except ValueError as e:
        # Captura o erro de produto não encontrado do CRUD e retorna um 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Lista os pedidos.
    - Admins: Veem todos os pedidos.
    - Users: Veem apenas os seus próprios pedidos.
    """
    if current_user.role == schemas.Role.ADMIN.value:
        orders = crud.get_all_orders(db, skip=skip, limit=limit)
    else:
        orders = crud.get_orders_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return orders


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_single_order(
    order_id: int,
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Busca um pedido específico por ID.
    - Admins: Podem ver qualquer pedido.
    - Users: Podem ver apenas os seus próprios pedidos.
    """
    order = crud.get_order_by_id(db, order_id=order_id)
    
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")

    if current_user.role != schemas.Role.ADMIN.value and order.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
        
    return order