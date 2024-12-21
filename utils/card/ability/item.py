from utils.card.card import ItemCard

# モンスターボール
class Monsterball(ItemCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)


    def check_available(self, field1, field2):
        return field1.stock.get_remaining_cards() > 0

    def __call__(self, field1, field2):
        # デッキからたねポケモンを1枚引く
        basic_pokemon = field1.stock.draw_basic_pokemon()
        if basic_pokemon is not None:
            field1.hand.add_card(basic_pokemon)
        return 

# スピーダー
class Speeder(ItemCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)

    def check_available(self, field1, field2):
        # スピーダーは常に使用可能
        return True

    def __call__(self, field1, field2):
        field1.battle.escape_energy["ス"] += 1
        return

# きずぐすり
class Potion(ItemCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)
    
    def check_available(self, field1, field2):
        # ポケモンのHPが満タンの時は使えない
        pokemon_list = [field1.battle.get_battle_pokemon()] + field1.bench.get_bench_pokemon()
        for pokemon in pokemon_list:
            if pokemon.hp < pokemon.max_hp:
                return True
        return False

    def __call__(self, field1, field2):
        pokemon_list = [field1.battle.get_battle_pokemon()] + field1.bench.get_bench_pokemon()
        eligible_pokemon = []
        for pokemon in pokemon_list:
            if pokemon.hp < pokemon.max_hp:
                eligible_pokemon.append(pokemon)
        for i, pokemon in enumerate(eligible_pokemon):
            print(f"{i+1}. {pokemon.name} HP:{pokemon.hp}/{pokemon.max_hp}")
        print("どのポケモンに使用しますか")
        while True:
            user_input = input()
            if not user_input.isdigit():
                print("無効な入力です。もう一度入力してください")
                continue
            user_input = int(user_input) - 1
            if user_input < len(eligible_pokemon):
                break
            print("無効な入力です。もう一度入力してください")
        selected_pokemon = eligible_pokemon[user_input]
        selected_pokemon.hp += 20
        return
