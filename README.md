

<h1 align="center">Weather Fasion</h1>


<p align="center">天気情報から服を提案するサービス</p>

<p align="center">
  <a href="https://github.com/mae-gaku/Weather-Cloth/releases"><img src="https://img.shields.io/github/v/release/mae-gaku/Weather-Cloth?style=flat-square" alt="Version"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square" alt="License"></a>

</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/41bb3c1f-2dc7-4da6-98ec-e202c8712e41" alt="MBI Logo" width="193" height="422" >
</p>



## 🚀 デモ

👉 [GitHub Pages でアプリを見る](https://mae-gaku.github.io/Weather-Fasion.github.io/)

---

## ToDo
- [ ] シンプルでUIデザイン
- [x] サインアップ・ログイン機能作成
- [ ] データベース管理
- [ ] 服装データ追加
- [ ] 服装レコメンドAI機能
- [ ] Try on AI開発


```sh
uvicorn app.main:app --reload
```

```sh
python3 init_db.py
```



```sh
python3 -m app.models
python3 -m app.seed_data
python3 -m app.scripts.generate_training_data
python3 -m app.scripts.train
```
