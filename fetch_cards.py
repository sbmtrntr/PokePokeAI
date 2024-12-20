import requests
import json
import time

# ベースURL
BASE_URL = "https://api.pokepoke-tcg.com/v1"

# 保存先のJSONファイル名
OUTPUT_FILE = "statics/cards/status2.json"

# 各カードセットのID範囲
CARD_SETS = {
    "A1": (1, 286),
    "PA": (1, 24)
}

# 結果を格納するリスト
all_cards = []

# カードデータを取得する関数
def fetch_card_data(set_id, card_id):
    url = f"{BASE_URL}?id={set_id}-{str(card_id).zfill(3)}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching card ID {set_id}-{str(card_id).zfill(3)}: {e}")
        return None

# カードセットごとのデータを取得する関数
def fetch_card_set_data(set_id, start_id, end_id):
    for card_id in range(start_id, end_id + 1):
        print(f"Fetching card ID {set_id}-{str(card_id).zfill(3)}...")
        card_data = fetch_card_data(set_id, card_id)
        if card_data:
            all_cards.extend(card_data)  # データをリストに追加
        time.sleep(0.5)  # APIサーバーへの負荷を軽減するためのウェイト

# メイン処理
def main():
    for set_id, (start_id, end_id) in CARD_SETS.items():
        fetch_card_set_data(set_id, start_id, end_id)

    # JSONファイルに保存
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_cards, f, ensure_ascii=False, indent=4)

    print(f"Finished fetching cards. Data saved to {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()