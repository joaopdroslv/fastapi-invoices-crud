from app.exceptions import NotFound
from app.models.user_model import User

from sqlalchemy.orm import Session


def find_user_by_id(user_id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFound('User')
    return user
