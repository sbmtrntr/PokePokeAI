class Choice:
    def __init__(self, field):
        self.field = field
        self.battle_field = field.battle_field
        self.battle_pokemon = field.battle_field.get_battle_pokemon()
        self.bench = field.bench.get_bench()
        self.hand = field.hand.get_hand()
        self.energy_current, self.energy_next = field.energy_zone.get_energy()
        self.choice = None
    
    def select_choice(self, index):
        move = self.choices[index]

        if move == "逃げる":
            escape(self.battle_pokemon)
        elif move == "たねポケモンをベンチに出す":
            hand2bench(self.battle_pokemon)
        elif move == "サポートカードを使用する":
            support(self.battle_pokemon)
        elif move == "グッズを使用する":
            gadget(self.battle_pokemon)
        elif move == "特性を使用する":
            ability(self.battle_pokemon)
        elif move == "エネルギーをつける":
            energy(self.battle_pokemon)
        elif move == "攻撃する":
            attack(self.battle_pokemon)

    
    def display_choice(self):
        self.choices = ["ターンを終了", "降参"]

        if self.can_escape():
            self.choices.append("逃げる")
        if self.can_hand2bench():
            self.choices.append("たねポケモンをベンチに出す")
        if self.can_use_support():
            self.choices.append("サポートカードを使用する")
        if self.can_use_item():
            self.choices.append("グッズを使用する")
        if self.can_use_ability():
            self.choices.append("特性を使用する")
        if self.can_attach_energy():
            self.choices.append("エネルギーをつける")
        if self.can_attack(): # 攻撃は必ず最後に表示
            self.choices.append("攻撃する")

        for i, choice in enumerate(self.choices):
            print(f"{i+1}. {choice}")
    
    def can_escape(self):
        # 逃げエネ <= エネルギーの合計 + 逃げエネ軽減カードの効果
        if self.battle_pokemon.convertedRetreatCost <= sum([value for value in self.battle_pokemon.energy.values()]) + self.battle_field.escape_energy:
            return True
        else:
            return False
    
    def can_hand2bench(self):
        for pokemon in self.hand:
            if pokemon.stage == "たね":
                return True    
        return False

                
    def can_use_support(self):
        for card in self.hand:
            if self.field.used_support == False and card.category == "トレーナーズ" and card.subCategory == "サポート" :
                return True
        return False
    

    def can_use_item(self):
        for card in self.hand:
            if card.category == "トレーナーズ" and card.subCategory == "グッズ":
                return True
        return False
    
    def can_use_ability(self):
        for pokemon in [self.battle_pokemon] + self.bench:
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

            
# 逃げる
def escape(pokemon):
    pokemon.hp = 0
    print(f"{pokemon.name}は逃げ出した")
    return pokemon

# ベンチに出す
def hand2bench(pokemon):
    pokemon.hp = 0
    print(f"{pokemon.name}はベンチに出した")
    return pokemon

# 攻撃する
def attack(pokemon):
    print(f"{pokemon.name}は攻撃した")
    return pokemon


# サポートカードを使用する
def support(pokemon):
    print(f"{pokemon.name}はサポートカードを使用した")
    return pokemon

# グッズを使用する
def gadget(pokemon):
    print(f"{pokemon.name}はグッズを使用した")
    return pokemon


# 特性を使用する
def ability(pokemon):
    print(f"{pokemon.name}は特性を使用した")
    return pokemon

# エネルギーをつける
def energy(pokemon):
    print(f"{pokemon.name}はエネルギーをつけた")
    return pokemon
