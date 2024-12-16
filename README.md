## ポケポケの対戦AI
を作りたい

## Todo
- [x] すべてのカードのステータス・効果を`statics/cards/status.yaml`に記載する
    - 有志の方のAPIを使わせてもらった
        - https://note.com/plan_sssss/n/n01fabe8eb739
        - 最新で追加されたカードの反映はまだのよう

- [x] デッキを取得できるようにする
    - `statics/template_decks.json`にテンプレートデッキの情報を記載

- [x] デッキから初期手札を取得できるようにする
    - `function.py`の`get_initial_hand`関数を作成
        - デッキからたねポケモンを1枚引く
        - デッキからランダムに4枚引く

- [ ] 先手・後手を選択できるようにする
    - エネルギーを導入する

- [ ] グッズとサポートの効果をデッキに反映させる

- [ ] 考え中

- [ ] ゲーム画面のキャプチャからゲームの状態を取得できるようにする
    - カードの画像を機械学習モデルに読み込ませて、どのカードか判定する
        - すべてのカードの画像を取得する必要あり `statics/cards/images/{number}.png`
    - もしくは、通信をキャプチャして、カードを判定する

- [ ] 盤面から最善手を選択できるようにする（最終目標）

## 環境構築
```bash
conda create -n pokepoke python=3.9
conda activate pokepoke
pip install -r requirements.txt
```