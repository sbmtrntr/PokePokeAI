import json
import random

# JSONファイルをロード
def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# デッキリストからカード情報を取得
def get_card_info(deck, all_cards):
    deck_info = []
    for card_id in deck:
        card = next((c for c in all_cards if c["id"] == card_id), None)
        if card:
            deck_info.append(card)
        else:
            print(f"Warning: Card '{card_id}' not found in the dataset.")
    return deck_info

# デッキ情報からランダムにたねポケモンを選ぶ
def select_basic_pokemon(deck_info):
    basic_pokemons = [card for card in deck_info if card.get("stage") == "たね"]
    if not basic_pokemons:
        print("No basic Pokémon found in the deck.")
        return None
    selected_pokemon = random.choice(basic_pokemons)
    deck_info.remove(selected_pokemon)
    return selected_pokemon

# デッキからランダムに一枚引く
def draw_card(deck_info):
    selected_pokemon = random.sample(deck_info, 1)[0]
    deck_info.remove(selected_pokemon)
    return selected_pokemon

# 最初の手札を取得
def get_initial_hand(hand, deck_info):
    hand.append(select_basic_pokemon(deck_info))
    for _ in range(4):
        hand.append(draw_card(deck_info))
    return hand

def debug_print(hand, deck_info):
    print("---手札---")
    for card in hand:
        print(card["name"])
    print("---山札---")
    for card in deck_info:
        print(card["name"])