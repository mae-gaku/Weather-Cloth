from fastapi import FastAPI, Request, Query, Depends, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.weather import get_weather_data
from app.recommender import recommend_outfits
from app.models import get_all_categories
from app.database import SessionLocal  # 追加
import uvicorn

from app.crud import get_outfits_by_category
from app.utils.scorer import score_outfit  # ← 作成したスコア関数
from app.models import Outfit

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# DBセッションを取得するための依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def suggest_outfit(weather_text: str, temp_max, temp_min, pop=None):
    if temp_max is None:
        return "気温情報が取得できませんでした。"

    if "雨" in weather_text or (pop is not None and pop >= 50):
        return "レインコートや防水ジャケットがあると安心です。"
    elif "雪" in weather_text:
        return "防寒と滑り止め対策が必要です！"
    elif "晴" in weather_text and int(temp_max) >= 25:
        return "Tシャツとハーフパンツなど軽装がオススメ！"
    elif int(temp_max) <= 10:
        return "コートやマフラーなど防寒対策を！"
    else:
        return "長袖のシャツや薄手のジャケットがおすすめです。"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    weather_data = await get_weather_data()
    suggestion = suggest_outfit(
        weather_text=weather_data["today_weather"],
        temp_max=weather_data["temp_max"],
        temp_min=weather_data["temp_min"],
        pop=weather_data.get("today_pop")
    )
    return templates.TemplateResponse("weather.html", {
        "request": request,
        "data": weather_data,
        "description": weather_data["today_weather"],
        "suggestion": suggestion,
        "pop": weather_data.get("today_pop"),
        "hourly": [],
        "forecast": []
    })


from app.utils.ai_scorer import predict_click_probability  # ← AIモデルベースのスコア関数

# @app.get("/outfits", response_class=HTMLResponse)
# async def outfits(request: Request, category: str, db: Session = Depends(get_db)):
#     weather_data = await get_weather_data()
#     outfits = db.query(Outfit).filter(Outfit.category.has(name=category)).all()

#     # AIでスコア算出
#     scored_outfits = sorted(
#         outfits,
#         key=lambda o: ai_score_outfit(o, weather_data, category),
#         reverse=True
#     )

#     return templates.TemplateResponse("outfits.html", {
#         "request": request,
#         "outfits": scored_outfits,
#         "category": f"{category}（おすすめ）",
#     })


# XGBoostモデルとエンコーダは起動時に読み込み
@app.get("/outfits", response_class=HTMLResponse)
async def outfits(request: Request, category: str, db: Session = Depends(get_db)):
    weather = await get_weather_data()
    outfits = db.query(Outfit).filter(Outfit.category.has(name=category)).all()

    # 予測スコア（クリックされる確率）で並べ替え
    scored = sorted(outfits, key=lambda o: predict_click_probability(o, weather), reverse=True)

    return templates.TemplateResponse("outfits.html", {
        "request": request,
        "outfits": scored,
        "category": f"{category}（おすすめ）",
    })


@app.get("/categories", response_class=HTMLResponse)
async def select_category(request: Request, db: Session = Depends(get_db)):
    categories = get_all_categories(db)  # dbを渡す
    category_list = [c[0] for c in categories]  # [('casual',), ('formal',)] → ['casual', 'formal']
    return templates.TemplateResponse("categories.html", {
        "request": request,
        "categories": category_list
    })





if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
