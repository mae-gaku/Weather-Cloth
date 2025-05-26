from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.orm import relationship

class Outfit(Base):
    __tablename__ = "outfits"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    image_url = Column(String)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="outfits")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    outfits = relationship("Outfit", back_populates="category")



# ↓↓↓↓ 追加する関数 ↓↓↓↓
from sqlalchemy.orm import Session

def get_all_categories(db: Session):
    return db.query(Outfit.category).distinct().all()


# models.py の末尾に以下を追加
if __name__ == "__main__":
    from app.database import engine
    Base.metadata.create_all(bind=engine)