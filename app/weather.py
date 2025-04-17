import httpx

# 東京の地域コードに対応するJSON（関東地方）
JMA_FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

async def get_weather_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(JMA_FORECAST_URL)
        data = response.json()

    # 天気は、data[0]["timeSeries"][0]["areas"][0]["weathers"]
    weathers = data[0]["timeSeries"][0]["areas"][0]["weathers"]
    temps = data[1]["timeSeries"][0]["areas"][0]  # max, min 温度など

    return {
        "today_weather": weathers[0],
        "tomorrow_weather": weathers[1],
        "temp_max": temps.get("max", [None])[0],
        "temp_min": temps.get("min", [None])[0],
    }
