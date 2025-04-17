from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.weather import get_weather_data
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")


def suggest_outfit(weather_text: str, temp_max, temp_min):
    print("temp_max", temp_max)
    if temp_max is None:
        return "気温情報が取得できませんでした。"

    # 優先度順にチェック（複数あるときは先に当たった方を採用）
    if "雨" in weather_text:
        return "レインコートや防水ジャケットがあると安心です。"
    elif "雪" in weather_text:
        return "防寒と滑り止め対策が必要です！"
    elif "晴" in weather_text and temp_max >= 25:
        return "Tシャツとハーフパンツなど軽装がオススメ！"
    elif temp_max <= 10:
        return "コートやマフラーなど防寒対策を！"
    else:
        return "長袖のシャツや薄手のジャケットがおすすめです。"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    weather_data = await get_weather_data()
    print("weather_data", weather_data)
    suggestion = suggest_outfit(
        weather_data["today_weather"],
        weather_data["temp_max"],
        weather_data["temp_min"]
    )
    return templates.TemplateResponse("weather.html", {
        "request": request,
        "data": weather_data,
        "description": weather_data["today_weather"],
        "suggestion": suggestion,
        "hourly": [],
        "forecast": []
    })

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
