# crud.py
from sqlalchemy.orm import Session
from app.models import Outfit

def get_outfits_by_category(db: Session, category: str):
    return db.query(Outfit).filter(Outfit.category.has(name=category)).all()


