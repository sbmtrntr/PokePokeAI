import requests
import json
import time

# ベースURL
BASE_URL = "https://api.pokepoke-tcg.com/v1"

# 保存先のJSONファイル名
OUTPUT_FILE = "statics/cards/status.json"

# カードIDの範囲
START_ID = 1
END_ID = 286

# 結果を格納するリスト
all_cards = []

# カードデータを取得する関数
def fetch_card_data(card_id):
    url = f"{BASE_URL}?id=A1-{str(card_id).zfill(3)}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching card ID A1-{str(card_id).zfill(3)}: {e}")
        return None

# メイン処理
for card_id in range(START_ID, END_ID + 1):
    print(f"Fetching card ID A1-{str(card_id).zfill(3)}...")
    card_data = fetch_card_data(card_id)
    if card_data:
        all_cards.extend(card_data)  # データをリストに追加
    time.sleep(0.5)  # APIサーバーへの負荷を軽減するためのウェイト

# JSONファイルに保存
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(all_cards, f, ensure_ascii=False, indent=4)

print(f"Finished fetching cards. Data saved to {OUTPUT_FILE}.")