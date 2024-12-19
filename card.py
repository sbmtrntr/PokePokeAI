from collections import defaultdict
from ability.support import *

class Card:
    def __init__(self, category, name):
        self.category = category
        self.name = name
    
    def display_card(self):
        raise NotImplementedError("This method should be implemented in subclasses")


class PokemonCard(Card):
    def __init__(self, name, stage, type, evolvesFrom, hp, attacks, weakness, convertedRetreatCost, ability):
        super().__init__("ポケモン", name)
        self.stage = stage
        self.type = type
        self.evolvesFrom = evolvesFrom
        self.max_hp = hp
        self.hp = hp
        self.attacks = attacks
        self.weakness = weakness
        self.convertedRetreatCost = convertedRetreatCost
        self.energy = defaultdict(int)
        self.ability = ability
    
    def display_card(self):
        WIDTH = 16
        # 枠の上部
        print(f"+{'ー' * WIDTH}+")
        # 名前、HP、タイプを表示
        print(f" {self.name:<6} HP:{self.hp}/{self.max_hp}    {self.type:}タイプ ")

        # 技の表示
        for attack in self.attacks:
            # 攻撃のエネルギーコストを連結
            energies = ''.join(attack['cost'])
            print(f" {energies:<6} {attack['name']:^6} ({attack['damage']}) ")

        # 弱点、逃げエネ、エネルギー表示
        print(f" 弱点:{self.weakness:<5}  逃げエネ:{self.convertedRetreatCost:<5} エネ:{''.join([energy_type * num for energy_type, num in self.energy.items()])} ")

        # 枠の下部
        print(f"+{'ー' * WIDTH}+\n")
    
    def use_ability(self):
        print(f"{self.ability[0]['name']}を使用")
    

class TrainerCard(Card):
    def __init__(self, name, subCategory, text):
        super().__init__("トレーナーズ", name)
        self.subCategory = subCategory
        self.text = text
    
    def display_card(self):
        WIDTH = 15
        # 枠の上部
        print(f"+{'ー' * WIDTH}+")
        print(f"{self.name} ({self.subCategory})")
        print(f"{self.text}")
        # 枠の下部
        print(f"+{'ー' * WIDTH}+\n")

class ItemCard(TrainerCard):
    def __init__(self, name, subCategory, text):
        super().__init__(name, subCategory, text)
        self.subCategory = "アイテム"

    def use(self, field):
        print(f"{self.name}を使用")

class SupportCard(TrainerCard):
    def __init__(self, name, subCategory, text):
        super().__init__(name, subCategory, text)
        self.subCategory = "サポート"

    def use(self, field):
        print(f"{self.name}を使用")
        if self.name == "博士の研究":
            field = professor_research(field)
        elif self.name == "エリカ":
            field = erika(field)
        return field