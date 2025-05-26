from sqlalchemy.orm import Session
from app.models import Outfit, Category
from app.database import SessionLocal

def seed_outfits(db: Session):
    casual = Category(name="カジュアル")
    clean = Category(name="キレイめ")
    normcore = Category(name="ノームコア")
    tech = Category(name="テック")

    db.add_all([casual, clean, normcore, tech])
    db.flush()  # IDを取得するため

    outfits = [
        Outfit(title="デニムと白T", image_url="/static/images/casual_001.jpg", description="動きやすい定番コーデ", category=casual),
        Outfit(title="パーカー＋チノパン", image_url="/static/images/casual_001.jpg", description="ゆるっとした休日スタイル", category=casual),
        Outfit(title="シャツ＋スラックス", image_url="/static/images/clean_001.jpg", description="上品な印象", category=clean),
        Outfit(title="テックジャケット＋ナイロンパンツ", image_url="/static/images/tech_001.jpg", description="機能性重視", category=tech),
        Outfit(title="normcore", image_url="/static/images/normcore_001.jpg", description="ゆるっとした", category=normcore),
    ]
    db.add_all(outfits)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    seed_outfits(db)
    db.close()
