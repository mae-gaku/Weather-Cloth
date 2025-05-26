import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# データ読み込み
df = pd.read_csv("training_data.csv")

# 前処理：カテゴリ変数のエンコード
le_category = LabelEncoder()
df["category"] = le_category.fit_transform(df["category"])

# 特徴量と目的変数に分割
X = df[[
    "temp_max", "temp_min", "pop",
    "category", "nylon_flag", "tshirt_flag", "jacket_flag"
]]
y = df["clicked"]

# データ分割
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# モデル学習
model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_train, y_train)

# 予測と評価
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Accuracy: {accuracy:.2f}")


import joblib
joblib.dump(model, "model.pkl")



joblib.dump(df["category"], "click_model.pkl")