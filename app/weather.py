import httpx

# JMAの地域コード辞書
AREA_CODES = {
    "東京": "130000",
    "大阪": "270000",
    "札幌": "016000",
    "福岡": "400000",
}

async def get_weather_data(location: str = "東京"):
    area_code = AREA_CODES.get(location, "130000")  # デフォルト東京
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    # --- 地方名と市区のマッピング（場所ごとに構造が違うので分岐） ---
    if location == "東京":
        weather_area_name = "東京地方"
        temp_area_name = "東京"
        pop_area_name = "東京地方"
    elif location == "大阪":
        weather_area_name = "大阪府"
        temp_area_name = "大阪"
        pop_area_name = "大阪府"
    elif location == "札幌":
        weather_area_name = "石狩地方"
        temp_area_name = "札幌"
        pop_area_name = "石狩地方"
    elif location == "福岡":
        weather_area_name = "福岡地方"
        temp_area_name = "福岡"
        pop_area_name = "福岡地方"

    # --- 天気 ---
    weather_areas = data[0]["timeSeries"][0]["areas"]
    weather_area = next(area for area in weather_areas if area["area"]["name"] == weather_area_name)
    weathers = weather_area["weathers"]

    # --- 気温 ---
    temp_areas = data[1]["timeSeries"][1]["areas"]
    temp_area = next(area for area in temp_areas if area["area"]["name"] == temp_area_name)
    temps_min = temp_area["tempsMin"]
    temps_max = temp_area["tempsMax"]

    # --- 降水確率 ---
    pop_areas = data[0]["timeSeries"][1]["areas"]
    pop_area = next(area for area in pop_areas if area["area"]["name"] == pop_area_name)
    pops = pop_area["pops"]

    today_pops = [int(p) for p in pops[:8] if p != ""]
    tomorrow_pops = [int(p) for p in pops[8:] if p != ""]

    today_pop_avg = sum(today_pops) // len(today_pops) if today_pops else None
    tomorrow_pop_avg = sum(tomorrow_pops) // len(tomorrow_pops) if tomorrow_pops else None

    return {
        "name": location,
        "today_weather": weathers[0],
        "tomorrow_weather": weathers[1],
        "temp_min": temps_min[1],
        "temp_max": temps_max[1],
        "today_pop": today_pop_avg,
        "tomorrow_pop": tomorrow_pop_avg,
        "weather_icon": "sunny",  # シンプルに仮置き
        "weather_icon_emoji": "☀️",
    }
