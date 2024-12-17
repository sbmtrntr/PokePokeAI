import json
import random

# JSONファイルをロード
def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

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

    cards = []
    for card_id in deck["カードid"]:
        card = next((c for c in all_cards if c["id"] == card_id), None)
        if card:
            cards.append({
                "name": card.get("name"),
                "evolvesFrom": card.get("evolvesFrom"),
                "stage": card.get("stage"),
                "type": card.get("type"),
                "weakness": card.get("weakness"),
                "max_hp": card.get("hp"),
                "hp": card.get("hp"),
                "attacks": card.get("attacks"),
                "retreatCost": card.get("retreatCost"),
                "convertedRetreatCost": card.get("convertedRetreatCost")
            })
        else:
            print(f"Warning: Card '{card_id}' not found in the dataset.")
    
    random.shuffle(cards)
    return cards

class Stock:
    def __init__(self, deck_name):
        self.cards = get_stock(deck_name)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)
        else:
            print("山札が空です。")

    def get_remaining_cards(self):
        return len(self.cards)
    
    def draw_basic_pokemon(self):
        """山札からランダムにたねポケモンを1枚引く"""
        basic_pokemons = [card for card in self.cards if card.get("stage") == "たね"]
        if not basic_pokemons:
            print("No basic Pokémon found in the deck.")
            return None
        selected_pokemon = random.choice(basic_pokemons)
        self.cards.remove(selected_pokemon)
        return selected_pokemon
    
    def get_initial_hand(self):
        """初期手札（たねポケモン1枚 + ランダム4枚）を取得"""
        cards = []
        # たねポケモン1枚を確保
        basic_pokemon = self.draw_basic_pokemon()
        if basic_pokemon:
            cards.append(basic_pokemon)
        else:
            print("デッキにたねポケモンがありません。")
        
        # 残り4枚をランダムに引く
        for _ in range(4):
            card = self.draw_card()
            if card:
                cards.append(card)
        return cards


class Hand:
    """手札クラス"""
    def __init__(self, stock):
        self.cards = stock.get_initial_hand()
    
    def add_card(self, stock):
        """山札から1枚カードを追加"""
        card = stock.draw_card()
        if card:
            self.cards.append(card)

    def display_hand(self):
        """手札の内容を表示"""
        print("\n【手札】")
        for i, card in enumerate(self.cards, 1):
            print(f"{i}: {card['name']} (HP: {card['hp']})")
        print("----------------------------")

    def get_hand(self):
        return self.cards
    
    def select_basic_pokemon(self):
        """手札からたねポケモンを選択"""
        basic_pokemons = [card for card in self.cards if card.get("stage") == "たね"]
        if not basic_pokemons:
            print("手札にたねポケモンがありません。")
            return None
        selected_pokemon = random.choice(basic_pokemons)
        self.cards.remove(selected_pokemon)
        return selected_pokemon


class BattleField:
    def __init__(self, hand):
        self.battle_pokemon = hand.select_basic_pokemon()  # バトル場

    def set_battle_pokemon(self, hand):
        """バトル場にポケモンをセット"""
        self.battle_pokemon = hand.select_basic_pokemon()

    def get_battle_pokemon(self):
        return self.battle_pokemon

    def swap_with_bench(self, bench, index):
        """バトル場とベンチのポケモンを入れ替える"""
        if 0 <= index < len(bench.bench_pokemons):
            bench_pokemon = bench.bench_pokemons[index]
            bench.bench_pokemons[index] = self.battle_pokemon
            self.battle_pokemon = bench_pokemon
        else:
            print("無効なベンチポケモンのインデックスです。")


class Bench:
    def __init__(self, capacity=3):
        self.capacity = capacity
        self.bench_pokemons = []

    def add_pokemon(self, hand):
        if len(self.bench_pokemons) < self.capacity:
            self.bench_pokemons.append(hand.select_basic_pokemon())
        else:
            print("ベンチが満杯です。")

    def get_bench(self):
        return self.bench_pokemons


class EnergyZone:
    def __init__(self, energy_type):
        self.energy = {energy: 0 for energy in energy_type}

    def attach_energy(self, energy):
        self.energy[energy] += 1

    def get_energy(self):
        return self.energy


class Field:
    def __init__(self, player_name, deck_name, energy_type):
        self.player_name = player_name
        self.stock = Stock(deck_name)
        self.hand = Hand(self.stock)
        self.battle_field = BattleField(self.hand)
        self.bench = Bench()
        self.energy_zone = EnergyZone(energy_type)

    def display_field(self):
        print(f"\n--- {self.player_name} のフィールド状況 ---")
        print("【バトルポケモン】")
        print(self.battle_field.get_battle_pokemon() or "なし")

        print("\n【ベンチポケモン】")
        for i, pokemon in enumerate(self.bench.get_bench()):
            print(f"ベンチ{i+1}: {pokemon}")

        print("\n【手札】")
        for i, card in enumerate(self.hand.get_hand()):
            print(f"手札{i+1}: {card}")

        print("\n【エネルギーゾーン】")
        print(", ".join(f"{energy}: {count}" for energy, count in self.energy_zone.get_energy().items()) or "なし")

        print(f"\n【山札の残り枚数】 {self.stock.get_remaining_cards()}")
        print("----------------------------")