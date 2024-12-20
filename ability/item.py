from utils.card import ItemCard

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
        field1.battle_field.escape_energy += 1
        return

# きずぐすり
class Potion(ItemCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)
    
    def check_available(self, field1, field2):
        # バトルポケモンのHPが満タンの時は使えない
        return field1.battle_field.get_battle_pokemon().hp < field1.battle_field.get_battle_pokemon().max_hp

    def __call__(self, field1, field2):
        field1.battle_field.get_battle_pokemon().hp += 20
        return
