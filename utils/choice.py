from utils.card import *

def display_choice(field1, field2, turn):
    choices = ["ターンを終了", "降参"]

    if can_escape(field1):
        choices.append("逃げる")
    if can_hand2bench(field1):
        choices.append("たねポケモンをベンチに出す")
    if can_evolve(field1, turn):
        choices.append("進化する")
    if can_use_support(field1, field2):
        choices.append("サポートカードを使用する")
    if can_use_item(field1):
        choices.append("グッズを使用する")
    if can_use_ability(field1):
        choices.append("特性を使用する")
    if can_attach_energy(field1):
        choices.append("エネルギーをつける")
    if can_attack(field1):
        choices.append("攻撃する")

    for i, choice in enumerate(choices):
        print(f"{i+1}. {choice}")
    
    return choices

def can_escape(field):
    # ベンチが空の場合は逃げられない
    if len(field.bench.get_bench_pokemon()) == 0:
        return False
    # 逃げエネ <= エネルギーの合計 + 逃げエネ軽減カードの効果
    if field.battle_field.get_battle_pokemon().convertedRetreatCost <= sum([value for value in field.battle_field.get_battle_pokemon().energy.values()]) + field.battle_field.escape_energy:
        return True
    else:
        return False

def can_hand2bench(field):
    # ベンチが満タンの場合は出せない
    if len(field.bench.get_bench_pokemon()) == 3:
        return False
    for card in field.hand.get_hand():
        if isinstance(card, PokemonCard) and card.stage == "たね":
            return True    
    return False

def can_evolve(field, turn):
    # 2ターン目までは進化できない
    if turn <= 2:
        return False
    pokemon_names = [field.battle_field.get_battle_pokemon().name] + [pokemon.name for pokemon in field.bench.get_bench_pokemon()]
    for card in field.hand.get_hand():
        if isinstance(card, PokemonCard) and card.evolvesFrom in pokemon_names:
            # このターンに手札から出していないかつ進化していないポケモンがいる場合は進化できる
            for pokemon in [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon():
                if pokemon.name == card.evolvesFrom and not pokemon.has_been_hand_to_bench and not pokemon.has_evolved_this_turn:
                    return True
    return False

            
def can_use_support(field1, field2):
    # サポートカードを使用済みの場合は使用できない
    if field1.used_support:
        return False
    for card in field1.hand.get_hand():
        if isinstance(card, SupportCard) and card.check_available(field1, field2):
            return True
    return False


def can_use_item(field):
    for card in field.hand.get_hand():
        if isinstance(card, ItemCard):
            return True
    return False

def can_use_ability(field):
    for pokemon in [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon():
        if pokemon.ability is not None:
            return True
    return False

def can_attach_energy(field):
    energy_current, energy_next = field.energy_zone.get_energy()
    if energy_current is not None:
        return True
    else:
        return False
    
def can_attack(field):
    for attack in field.battle_field.get_battle_pokemon().attacks:
        # 必要なエネルギーコストをコピーして計算用に保持
        required_cost = attack['cost'].copy()
        available_energy = field.battle_field.get_battle_pokemon().energy.copy()

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