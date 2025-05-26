import csv
from app.database import SessionLocal
from app.models import Outfit
import random

# 仮の気象データ（本番では実データと紐づける）
def generate_weather_data():
    return {
        "temp_max": random.choice(range(10, 35)),
        "temp_min": random.choice(range(0, 25)),
        "pop": random.choice(range(0, 100))
    }

def extract_features(outfit, weather):
    return {
        "temp_max": weather["temp_max"],
        "temp_min": weather["temp_min"],
        "pop": weather["pop"],
        "category": outfit.category.name if outfit.category else "",
        "title": outfit.title,
        "description": outfit.description,
        "nylon_flag": int("ナイロン" in outfit.description),
        "tshirt_flag": int("Tシャツ" in outfit.title or "Tシャツ" in outfit.description),
        "jacket_flag": int("ジャケット" in outfit.title or "ジャケット" in outfit.description),
        "clicked": random.choice([0, 1])  # 本番では実データで
    }

def main():
    db = SessionLocal()
    outfits = db.query(Outfit).all()

    with open("training_data.csv", "w", newline='', encoding='utf-8') as csvfile:
        fieldnames = ["temp_max", "temp_min", "pop", "category", "title", "description",
                      "nylon_flag", "tshirt_flag", "jacket_flag", "clicked"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for outfit in outfits:
            weather = generate_weather_data()
            features = extract_features(outfit, weather)
            writer.writerow(features)

    print("✅ training_data.csv 作成完了")

if __name__ == "__main__":
    main()
