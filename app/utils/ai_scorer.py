# utils/ai_scorer.py

import joblib
import numpy as np
import os
import pickle
import pandas as pd

# モデル読み込み（例：LightGBMモデル）
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(model_path)

# カテゴリを数値に変換（仮：本番ではLabelEncoder使う）
CATEGORY_MAP = {
    "カジュアル": 0,
    "キレイめ": 1,
    "ノームコア": 2,
    "テック": 3
}

def extract_features(outfit, weather_data, category: str):
    return [
        int(weather_data["temp_max"] or 25),
        int(weather_data["temp_min"] or 15),
        int(weather_data["today_pop"] or 0),
        CATEGORY_MAP.get(category, -1),
        int("ナイロン" in outfit.description),
        int("Tシャツ" in outfit.title),
        int("ジャケット" in outfit.title),
    ]

def predict_click_probability(outfit, weather):
    from sklearn.preprocessing import LabelEncoder
    le_category = LabelEncoder()
    le_category.fit(["カジュアル", "キレイめ", "テック", "ノームコア"])

    features = {
        "temp_max": float(weather["temp_max"]) if weather["temp_max"] is not None else 25.0,
        "temp_min": float(weather["temp_min"]) if weather["temp_min"] is not None else 15.0,
        "pop": float(weather.get("today_pop", 0)) if weather.get("today_pop") is not None else 0.0,
        "category": int(le_category.transform([outfit.category.name])[0]),
        "nylon_flag": int("ナイロン" in outfit.description),
        "tshirt_flag": int("Tシャツ" in outfit.title or "Tシャツ" in outfit.description),
        "jacket_flag": int("ジャケット" in outfit.title or "ジャケット" in outfit.description)
    }

    input_df = pd.DataFrame([features])
    input_df = input_df.astype({
        "temp_max": "float64",
        "temp_min": "float64",
        "pop": "float64",
        "category": "int64",
        "nylon_flag": "int64",
        "tshirt_flag": "int64",
        "jacket_flag": "int64"
    })

    proba = model.predict_proba(input_df)[0][1]  # clicked=1 の確率
    print("proba", proba)
    return proba



# app/utils/ai_scorer.py

import joblib
import os
import pandas as pd

# モデルのロード
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(model_path)

# カテゴリ変換（本番はDBに対応させる）
CATEGORY_MAP = {
    "カジュアル": 0,
    "キレイめ": 1,
    "ノームコア": 2,
    "テック": 3
}

def suggest_by_ai(weather, category: str):
    features = {
        "temp_max": float(weather.get("temp_max", 25)),
        "temp_min": float(weather.get("temp_min", 15)),
        "pop": float(weather.get("today_pop", 0)),
        "category": CATEGORY_MAP.get(category, -1),
        "nylon_flag": 0,
        "tshirt_flag": 0,
        "jacket_flag": 0
    }
    input_df = pd.DataFrame([features])
    prob = model.predict_proba(input_df)[0][1]
    return prob
