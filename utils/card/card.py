from collections import defaultdict

class Card:
    def __init__(self, category, name):
        self.category = category
        self.name = name
    
    def display_card(self):
        raise NotImplementedError("This method should be implemented in subclasses")


class PokemonCard(Card):
    def __init__(self, name, cardRule, evolvesFrom, stage, type, hp, attacks, weakness, convertedRetreatCost, ability):
        super().__init__("ポケモン", name)
        self.cardRule = cardRule
        self.evolvesFrom = evolvesFrom
        self.stage = stage
        self.type = type
        self.hp = hp
        self.max_hp = hp
        self.attacks = attacks
        self.weakness = weakness
        self.convertedRetreatCost = convertedRetreatCost
        self.energy = defaultdict(int)
        self.ability = ability
        self.has_evolved_this_turn = False
        self.has_been_hand_to_bench= False

    def evolve(self, evolvesTo):
        self.cardRule = evolvesTo.cardRule
        self.name = evolvesTo.name
        self.stage = evolvesTo.stage
        self.type = evolvesTo.type
        self.evolvesFrom = evolvesTo.evolvesFrom
        self.hp = evolvesTo.hp - (self.max_hp - self.hp)
        self.max_hp = evolvesTo.max_hp
        self.attacks = evolvesTo.attacks
        self.weakness = evolvesTo.weakness
        self.convertedRetreatCost = evolvesTo.convertedRetreatCost
        self.ability = evolvesTo.ability
        self.has_evolved_this_turn = True
        self.has_been_hand_to_bench = False

    def display_card(self):
        WIDTH = 16
        # 枠の上部
        print(f"+{'ー' * WIDTH}+")
        # 名前、HP、タイプを表示
        print(f" {self.name:<6} HP:{self.hp}/{self.max_hp} {self.type:}タイプ ")

        # 技の表示
        for attack in self.attacks:
            # 攻撃のエネルギーコストを連結
            energies = ''.join([energy_type * num for energy_type, num in attack["cost"].items()])
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
    
    def check_available(self, field1, field2):
        """
        使用可能かどうかを判定するメソッド。
        各カードでオーバーライドする。
        """
        raise NotImplementedError("このメソッドはサブクラスで実装")

    def __call__(self, field1, field2):
        """
        カード効果を実行するメソッド。
        各カードでオーバーライドする。
        """
        raise NotImplementedError("このメソッドはサブクラスで実装")


class SupportCard(TrainerCard):
    def __init__(self, name, text):
        super().__init__(name=name, subCategory="サポート", text=text)

    def check_available(self, field1, field2):
        """
        使用可能かどうかを判定するメソッド。
        各カードでオーバーライドする。
        """
        raise NotImplementedError("このメソッドはサブクラスで実装")

    def __call__(self, field1, field2):
        """
        カード効果を実行するメソッド。
        各カードでオーバーライドする。
        """
        raise NotImplementedError("このメソッドはサブクラスで実装")


class ItemCard(TrainerCard):
    def __init__(self, name, text):
        super().__init__(name=name, subCategory="グッズ", text=text)
    
    def check_available(self, field1, field2):
        """
        使用可能かどうかを判定するメソッド。
        各カードでオーバーライドする。
        """
        raise NotImplementedError("このメソッドはサブクラスで実装")

    def __call__(self, field1, field2):
        """
        カード効果を実行するメソッド。
        各カードでオーバーライドする。
        """
        raise NotImplementedError("このメソッドはサブクラスで実装")