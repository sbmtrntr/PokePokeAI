## ポケポケの対戦AI
を作りたい
## Todo
- ゲーム画面のキャプチャからゲームの状態を取得できるか
    - カードの画像を機械学習モデルに読み込ませて、どのカードか判定する
        - すべてのカードの画像を取得する必要あり `statics/cards/images/{number}.png`
    - もしくは、通信をキャプチャして、カードを判定する
- カードのステータス・効果
    - すべてのカードのステータス・効果を`statics/cards/status.yaml`に記載する
- 強化学習でやるか、αβ法でやるか

## 環境構築
```bash
conda create -n pokepoke python=3.9
conda activate pokepoke
pip install -r requirements.txt
```