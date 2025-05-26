# utils/scorer.py

def score_outfit(outfit, weather_data):
    score = 0

    # 気温でスコア調整
    max_temp = int(weather_data["temp_max"] or 25)
    min_temp = int(weather_data["temp_min"] or 15)

    if "Tシャツ" in outfit.title or "Tシャツ" in outfit.description:
        if max_temp >= 25:
            score += 5
        else:
            score -= 2

    if "ジャケット" in outfit.title or "ジャケット" in outfit.description:
        if min_temp <= 15:
            score += 5
        else:
            score -= 2

    # 降水確率が高いならナイロン系を優遇
    pop = weather_data["today_pop"] or 0
    if pop >= 50 and "ナイロン" in outfit.description:
        score += 5
    print("score", score)
    return score
