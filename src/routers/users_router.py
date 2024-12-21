from src.database.dependencies import get_db
from src.models.user_model import User
from src.schemas.user_schema import UserRequest, UserResponse
from src.crud.user_crud import find_user_by_id

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(prefix='/users')


@router.get('/', response_model=List[UserResponse], status_code=200)
def list_users(db: Session = Depends(get_db)) -> List[UserResponse]:
    return db.query(User).all()


@router.get('/{user_id}', response_model=UserResponse, status_code=200)
def list_user(user_id: int , db: Session = Depends(get_db)) -> UserResponse:
    return find_user_by_id(user_id, db)


@router.post('/', response_model=UserResponse, status_code=201)
def create_user(provided_user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    new_user = User(**provided_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.put('/{user_id}', response_model=UserResponse, status_code=200)
def update_user(user_id: int, provided_user: UserRequest, db: Session = Depends(get_db)) -> UserResponse:
    user = find_user_by_id(user_id, db)

    user.first_name = provided_user.first_name
    user.last_name = provided_user.last_name  

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    user = find_user_by_id(user_id, db)
    db.delete(user)
    db.commit()
