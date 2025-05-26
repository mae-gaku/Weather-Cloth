from typing import List, Tuple
from sqlalchemy.orm import Session
from app.models import Outfit


def get_outfits_by_category(db: Session, category: str) -> List[Outfit]:
    """
    カテゴリ名に応じた洋服データを取得する。
    """
    return db.query(Outfit).join(Outfit.category).filter(Outfit.category.has(name=category)).all()


def recommend_outfits(
    db: Session,
    category: str,
    weather_text: str,
    temp_max: int,
    temp_min: int,
    pop: int = None
) -> List[dict]:
    """
    天気とカテゴリに基づいて、適した洋服リストを返す。
    """
    all_outfits = get_outfits_by_category(db, category)
    recommendations = []

    for outfit in all_outfits:
        if not is_suitable(outfit, weather_text, temp_max, pop):
            continue
        recommendations.append({
            "name": outfit.name,
            "image_url": outfit.image_url,
            "description": outfit.description or "",
        })

    # 上位6件まで返す（Pinterest風UIにちょうど良い）
    return recommendations[:6]


def is_suitable(outfit: Outfit, weather_text: str, temp_max: int, pop: int = None) -> bool:
    """
    その洋服が現在の天気に適しているか判定する。
    outfit には weather_tags, temp_range, rain_ok などの属性が含まれている前提
    """
    # 天気キーワードが一致しているか（晴れ/雨/雪など）
    if outfit.weather_tags:
        matched = any(tag in weather_text for tag in outfit.weather_tags)
        if not matched:
            return False

    # 気温範囲に合っているか
    if outfit.temp_range:
        min_temp, max_temp = outfit.temp_range
        if temp_max < min_temp or temp_max > max_temp:
            return False

    # 雨に適しているか（降水確率が高いとき rain_ok=True のものだけ）
    if pop is not None and pop >= 50:
        if not outfit.rain_ok:
            return False

    return True
