import random
from utils.card.card import PokemonCard, SupportCard, ItemCard
from utils.card.init_card import initialize_cards

class Stock:
    def __init__(self, deck_name):
        self.cards = initialize_cards(deck_name)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)
        else:
            print("山札が空です。")

    def get_remaining_cards(self):
        return len(self.cards)
    
    def get_stock(self):
        return self.cards
    
    def draw_basic_pokemon(self):
        """山札からランダムにたねポケモンを1枚引く"""
        basic_pokemons = [card for card in self.cards if isinstance(card, PokemonCard) and card.stage == "たね"]
        if not basic_pokemons:
            print("デッキにたねポケモンがありません。")
            return None
        selected_pokemon = random.choice(basic_pokemons)
        self.cards.remove(selected_pokemon)
        random.shuffle(self.cards)
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
    
    def add_card(self, pokemon):
        """カードを手札に追加"""
        self.cards.append(pokemon)

    def remove_card(self, card):
        """手札からカードを削除"""
        self.cards.remove(card)

    def display_hand(self):
        """手札の内容を表示"""
        print("\n【手札】")
        for i, card in enumerate(self.cards, 1):
            print(f"{i}: {card.name} (HP: {card.hp})")
        print("----------------------------")

    def get_hand(self):
        return self.cards
    
    def select_basic_pokemon(self):
        """手札からたねポケモンを選択"""
        basic_pokemons = [card for card in self.cards if isinstance(card, PokemonCard) and card.stage == "たね"]
        if not basic_pokemons:
            print("手札にたねポケモンがありません。")
            return None
        selected_pokemon = random.choice(basic_pokemons)
        self.cards.remove(selected_pokemon)
        return selected_pokemon
    
    def set_hand(self, hand):
        self.cards = hand


class Battle:
    def __init__(self, hand):
        self.battle_pokemon = hand.select_basic_pokemon()  # バトル場
        self.escape_energy = {"ス":0}

    def set_battle_pokemon(self, pokemon):
        """バトル場にポケモンをセット"""
        self.battle_pokemon = pokemon

    def get_battle_pokemon(self):
        return self.battle_pokemon
    
    def add_escape_energy(self):
        """逃げエネを追加"""
        self.escape_energy["ス"] += 1

    def escape_to_bench(self, bench, index):
        """バトル場のポケモンが逃げる"""
        required_energy = self.battle_pokemon.convertedRetreatCost
        # スピーダーが使われている場合は逃げエネを減らす
        if self.escape_energy["ス"] > 0:
            required_energy = min(0, required_energy - self.escape_energy["ス"])

        # バトル場のポケモンのエネルギーが1種類なら逃げエネ分エネルギーを消費
        if required_energy > 0 and len(self.battle_pokemon.energy) == 1:
            energy_type = list(self.battle_pokemon.energy.keys())[0]
            self.battle_pokemon.energy[energy_type] -= required_energy
        #複数のエネルギーがついている場合は消費するエネルギーを選択
        else:
            for _ in range(required_energy):
                for energy_type, num in self.battle_pokemon.energy.items():
                    print(f"{energy_type}: {num}個")
                    while True:
                        selected_energy_type = input("エネルギーを選択してください: ")
                        if selected_energy_type.isdigit():  # 文字列じゃない場合はcontinue
                            print("無効な入力です。もう一度入力してください")
                            continue
                        if selected_energy_type in self.battle_pokemon.energy:
                            break
                        print("無効な入力です。もう一度入力してください")
                self.battle_pokemon.energy[selected_energy_type] -= 1
        
        bench_pokemon = bench.bench_pokemons[index]
        bench.bench_pokemons[index] = self.battle_pokemon
        self.battle_pokemon = bench_pokemon


class Bench:
    def __init__(self, capacity=3):
        self.capacity = capacity
        self.bench_pokemons = []

    def add_pokemon(self, pokemon):
        if len(self.bench_pokemons) < self.capacity:
            self.bench_pokemons.append(pokemon)
            pokemon.has_been_hand_to_bench = True
        else:
            print("ベンチが満杯です。")

    def get_bench_pokemon(self):
        return self.bench_pokemons
    
    def remove_pokemon(self, pokemon):
        self.bench_pokemons.remove(pokemon)


class EnergyZone:
    def __init__(self, energy_type):
        self.energy_type = energy_type
        self.current_energy = None
        self.next_energy = random.choice(energy_type)

    def generate_energy(self):
        self.current_energy = self.next_energy
        self.next_energy = random.choice(self.energy_type)

    def attach_energy(self, pokemon):
        pokemon.energy[self.current_energy] += 1
        self.current_energy = None

    def get_energy(self):
        return self.current_energy, self.next_energy


class Field:
    def __init__(self, player_name, deck_name, energy_type):
        self.player_name = player_name
        self.point = 0
        self.stock = Stock(deck_name)
        self.hand = Hand(self.stock)
        self.battle = Battle(self.hand)
        self.bench = Bench()
        self.energy_zone = EnergyZone(energy_type)
        self.trash = []
        self.used_support = False
        self.attacked = False
        self.turn_end = False
        self.escaped = False
    
    def reset_turn(self):
        self.battle.escape_energy = {"ス":0}
        self.used_support = False
        self.hand.add_card(self.stock.draw_card())
        self.attacked = False
        self.turn_end = False
        self.escaped = False
        for pokemon in [self.battle.get_battle_pokemon()] + self.bench.get_bench_pokemon():
            pokemon.has_evolved_this_turn = False
            pokemon.has_been_hand_to_bench = False
            