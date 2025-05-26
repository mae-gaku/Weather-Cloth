import httpx

JMA_FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"

async def get_weather_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(JMA_FORECAST_URL)
        data = response.json()

    # 東京地方の天気
    weather_areas = data[0]["timeSeries"][0]["areas"]
    tokyo_weather_area = next(area for area in weather_areas if area["area"]["name"] == "東京地方")
    weathers = tokyo_weather_area["weathers"]

    # 東京の気温
    temp_areas = data[1]["timeSeries"][1]["areas"]
    tokyo_temp_area = next(area for area in temp_areas if area["area"]["name"] == "東京")
    temps_min = tokyo_temp_area["tempsMin"]
    temps_max = tokyo_temp_area["tempsMax"]

    # 東京地方の降水確率
    pop_areas = data[0]["timeSeries"][1]["areas"]
    tokyo_pop_area = next(area for area in pop_areas if area["area"]["name"] == "東京地方")
    pops = tokyo_pop_area["pops"]

    # 今日と明日の平均降水確率（前半8つが今日、後半4つが明日）
    today_pops = [int(p) for p in pops[:8] if p != ""]
    tomorrow_pops = [int(p) for p in pops[8:] if p != ""]

    today_pop_avg = sum(today_pops) // len(today_pops) if today_pops else None
    tomorrow_pop_avg = sum(tomorrow_pops) // len(tomorrow_pops) if tomorrow_pops else None

    return {
        "today_weather": weathers[0],
        "tomorrow_weather": weathers[1],
        "temp_min": temps_min[1],
        "temp_max": temps_max[1],
        "today_pop": today_pop_avg,
        "tomorrow_pop": tomorrow_pop_avg,
    }
