from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth

router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"],
)

@router.get("/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.get_current_active_user)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/", response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.RoleChecker([schemas.Role.ADMIN]))):
    db_product = crud.get_product_by_code(db, code=product.code)
    if db_product:
        raise HTTPException(status_code=400, detail="Código de produto já existe")
    return crud.create_product(db=db, product=product)

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.RoleChecker([schemas.Role.ADMIN]))):
    db_product = crud.update_product(db, product_id=product_id, product_update=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product

@router.delete("/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(auth.get_db), current_user: schemas.User = Depends(auth.RoleChecker([schemas.Role.ADMIN]))):
    db_product = crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product