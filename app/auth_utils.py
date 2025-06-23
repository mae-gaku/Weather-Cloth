# auth_utils.py（新規作成）

from fastapi import Request
from sqlalchemy.orm import Session
from .models import User

def get_current_user(request: Request, db: Session):
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return db.query(User).filter(User.id == user_id).first()
