# 一度だけ実行
from database import engine
from models import Base

# テーブル作成
Base.metadata.create_all(bind=engine)
