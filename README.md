

<h1 align="center">Weather Fasion</h1>


<p align="center">天気情報から服を提案するサービス</p>

<p align="center">
  <a href="https://github.com/mae-gaku/Weather-Cloth/releases"><img src="https://img.shields.io/github/v/release/mae-gaku/Weather-Cloth?style=flat-square" alt="Version"></a>
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square" alt="License"></a>

</p>


<p align="center">
  <img src="https://github.com/user-attachments/assets/eb7a1c4c-3cb7-4f33-9474-9e437eec24c8" alt="MBI Logo" width="300">
</p>


---

## ToDo
- [ ] シンプルでUIデザイン
- [ ] サインアップ・ログイン機能作成
- [ ] データベース管理


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