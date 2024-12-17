import json
import random

# JSONファイルをロード
def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# デッキリストからカード情報を取得
def get_stock(deck_name):
    # カードのステータスが保存されたJSONファイルのパス
    CARD_STATUS_FILE = "statics/cards/status.json"
    # カードデータをロード
    all_cards = load_json_file(CARD_STATUS_FILE)

    # テンプレートデッキJSONファイルのパス
    TEMPLATE_DECKS_FILE = "statics/template_decks.json"
    # テンプレートデッキをロード
    all_template_decks = load_json_file(TEMPLATE_DECKS_FILE)

    for deck in all_template_decks:
        if deck["デッキ名"] == deck_name:
            break

    stock = []
    for card_id in deck["カード"]:
        card = next((c for c in all_cards if c["id"] == card_id), None)
        if card:
            stock.append(card)
        else:
            print(f"Warning: Card '{card_id}' not found in the dataset.")
    return stock

# 山札からランダムにたねポケモンを選ぶ
def select_basic_pokemon(stock):
    basic_pokemons = [card for card in stock if card.get("stage") == "たね"]
    if not basic_pokemons:
        print("No basic Pokémon found in the deck.")
        return None
    selected_pokemon = random.choice(basic_pokemons)
    stock.remove(selected_pokemon)
    return selected_pokemon

# 山札からランダムに一枚引く
def draw_card(stock):
    selected_pokemon = random.sample(stock, 1)[0]
    stock.remove(selected_pokemon)
    return selected_pokemon

# 山札から最初の手札を取得
def get_initial_hand(stock):
    hand = []
    hand.append(select_basic_pokemon(stock))
    for _ in range(4):
        hand.append(draw_card(stock))
    return hand

def debug_print(hand, stock):
    print("---手札---")
    for card in hand:
        print(card["name"])
    print("---山札---")
    for card in stock:
        print(card["name"])