def suggest_outfit(temp: float, weather: str) -> str:
    if temp > 25:
        return "半袖シャツとショートパンツ、サングラスがぴったりです 😎"
    elif 20 <= temp <= 25:
        return "薄手のシャツとチノパンがおすすめです 👕"
    elif 15 <= temp < 20:
        return "軽めのジャケットを羽織ると快適です 🧥"
    elif 10 <= temp < 15:
        return "厚手のコートとマフラーが必要かもしれません 🧣"
    else:
        return "しっかり防寒対策！ダウンジャケットを着ましょう 🧤"

