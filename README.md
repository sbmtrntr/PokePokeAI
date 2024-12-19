## ポケポケの対戦AI
を作りたい

## Todo
- [x] すべてのカードのステータス・効果を`statics/cards/status.yaml`に記載する(12/16)
    - 有志の方のAPIを使わせてもらった
        - https://note.com/plan_sssss/n/n01fabe8eb739
        - 最新で追加されたカードの反映はまだのよう

- [x] デッキを取得できるようにする(12/16)
    - `statics/template_decks.json`にテンプレートデッキの情報を記載

- [x] デッキから初期手札を取得できるようにする(12/16)
    - デッキからたねポケモンを1枚引く
    - デッキからランダムに4枚引く

- [x] 先手・後手を選択できるようにする(12/17)
  
- [x] フィールドを表示できるようにする(12/17)
    - `field.py`の`Field`クラスを作成
    - Player1_field.display_field()で状況を表示

- [x] 選択肢を表示できるようにする(12/19)
    - `choice.py`の`Choice`クラスを作成
    - `choice.display_choice()`で選択肢を表示
  
- [ ] 行動できるようにする
    - [x] エネルギーをつける(12/19)
    - [x] 逃げる(12/19)
    - [x] たねポケモンをベンチに出す(12/19)
    - [ ] 進化する
    - [ ] サポートカードを使用する
    - [ ] グッズを使用する
    - [ ] 特性を使用する
    - [ ] 攻撃する
  
- [ ] ポケモン、グッズ、サポートの効果を反映させる
    - かなり面倒くさい作業なので、できたら人の手を借りたい
        - とりあえずフシギバナEXとリザードンEXで使われるカードの効果だけ完成させる
    - `ability/{}.py`に記載 

- [ ] 考え中
  
- [ ] コマンドラインで対戦できるようにする
    - シミュレーションで使うだけならいらない作業

- [ ] 盤面から最善手を選択できるようにする
    - とても時間がかかりそう

- [ ] ゲーム画面のキャプチャからゲームの状態を取得できるようにする（最終目標）
    - カードの画像を機械学習モデルに読み込ませて、どのカードか判定する
        - すべてのカードの画像を取得する必要あり `statics/cards/images/{number}.png`
    - もしくは、通信をキャプチャして、カードを判定する

## Usage
1. statics/template_decks.jsonに使いたいデッキを登録
2. main.pyの`Player1_field`と`Player2_field`を変更
3. コマンドラインで以下を実行
```bash
python main.py
```

## Environment
対戦するだけなら（今のところ）必要なし
```bash
conda create -n pokepoke python=3.9
conda activate pokepoke
pip install -r requirements.txt
```