# クラスにする必要がなかったのでリファクタリングしたい

class Choice:
    def __init__(self, field):
        self.field = field
        self.battle_field = field.battle_field
        self.battle_pokemon = field.battle_field.get_battle_pokemon()
        self.bench_pokemon = field.bench.get_bench_pokemon()
        self.hand_card = field.hand.get_hand()
        self.energy_current, self.energy_next = field.energy_zone.get_energy()
        self.choice = None
    
    def display_choice(self):
        choices = ["ターンを終了", "降参"]

        if self.can_escape():
            choices.append("逃げる")
        if self.can_hand2bench():
            choices.append("たねポケモンをベンチに出す")
        if self.can_use_support():
            choices.append("サポートカードを使用する")
        if self.can_use_item():
            choices.append("グッズを使用する")
        if self.can_use_ability():
            choices.append("特性を使用する")
        if self.can_attach_energy():
            choices.append("エネルギーをつける")
        if self.can_attack():
            choices.append("攻撃する")

        for i, choice in enumerate(choices):
            print(f"{i+1}. {choice}")
        
        return choices
    
    def can_escape(self):
        # ベンチが空の場合は逃げられない
        if len(self.bench_pokemon) == 0:
            return False
        # 逃げエネ <= エネルギーの合計 + 逃げエネ軽減カードの効果
        if self.battle_pokemon.convertedRetreatCost <= sum([value for value in self.battle_pokemon.energy.values()]) + self.battle_field.escape_energy:
            return True
        else:
            return False
    
    def can_hand2bench(self):
        # ベンチが満タンの場合は出せない
        if len(self.bench_pokemon) == 3:
            return False
        for card in self.hand_card:
            if card.category == "ポケモン" and card.stage == "たね":
                return True    
        return False

                
    def can_use_support(self):
        # サポートカードを使用済みの場合は使用できない
        if self.field.used_support:
            return False
        for card in self.hand_card:
            if card.category == "トレーナーズ" and card.subCategory == "サポート" :
                return True
        return False
    

    def can_use_item(self):
        for card in self.hand_card:
            if card.category == "トレーナーズ" and card.subCategory == "グッズ":
                return True
        return False
    
    def can_use_ability(self):
        for pokemon in [self.battle_pokemon] + self.bench_pokemon:
            if pokemon.ability is not None:
                return True
        return False
    
    def can_attach_energy(self):
        if self.energy_current is not None:
            return True
        else:
            return False
        
    def can_attack(self):
        for attack in self.battle_pokemon.attacks:
            # 必要なエネルギーコストをコピーして計算用に保持
            required_cost = attack['cost'].copy()
            available_energy = self.battle_pokemon.energy.copy()

            # 無色エネルギーのコストを取得
            colorless_cost = required_cost.pop("無", 0)

            # 各エネルギータイプのコストをチェック
            for energy_type, energy_cost in required_cost.items():
                if available_energy.get(energy_type, 0) < energy_cost:
                    # 必要エネルギーが足りない場合はこの攻撃はできない
                    break
                # 必要分を消費する（シミュレーション）
                available_energy[energy_type] -= energy_cost
            else:
                # 無色エネルギーの処理（他のエネルギーで代用可能）
                total_available_energy = sum(available_energy.values())
                if total_available_energy >= colorless_cost:
                    # 条件を満たす攻撃が1つでもあればTrueを返す
                    return True

        # どの攻撃も条件を満たさない場合
        return False