from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.invoice_model import Invoice
from app.models.user_model import User
from app.schemas.invoice_schema import InvoiceResponse
from app.schemas.user_schema import UserRequest, UserResponse
from app.service.user_service import find_user_by_id

router = APIRouter(prefix="/users")


@router.get("/", response_model=List[UserResponse], status_code=200)
def list_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def list_user(user_id: int, db: Session = Depends(get_db)) -> UserResponse:
    return find_user_by_id(user_id, db)


@router.get(
    "/{user_id}/invoices", response_model=List[InvoiceResponse], status_code=200
)
def list_user_invoices(
    user_id: int, db: Session = Depends(get_db)
) -> List[InvoiceResponse]:
    find_user_by_id(user_id, db)
    return db.query(Invoice).filter(Invoice.user_id == user_id).all()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    provided_user: UserRequest, db: Session = Depends(get_db)
) -> UserResponse:
    db_user = User(**provided_user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(
    user_id: int, provided_user: UserRequest, db: Session = Depends(get_db)
) -> UserResponse:
    db_user = find_user_by_id(user_id, db)

    db_user.first_name = provided_user.first_name
    db_user.last_name = provided_user.last_name

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    db_user = find_user_by_id(user_id, db)
    db.delete(db_user)
    db.commit()
