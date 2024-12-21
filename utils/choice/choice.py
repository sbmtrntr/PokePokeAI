from utils.card.card import *
from utils.choice.movement import *

def choice_action(my_field, opponent_field, turn):
    choices = display_choice(my_field, opponent_field, turn)
    while True:
        user_input = input("行動を選択してください: ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(choices):
            break
        print("無効な入力です。もう一度入力してください")
    
    if choices[index] == "ターンを終了": 
        my_field.turn_end = True

    elif choices[index] == "降参": 
        user_input = input("本当に降参しますか？(y/n): ")
        if user_input == "y":
            exit(print(f"{my_field.player_name}の負けです"))

    
    elif choices[index] == "エネルギーをつける":
        attach_energy(my_field)

    elif choices[index] == "逃げる":
        escape(my_field)

    elif choices[index] == "たねポケモンをベンチに出す":
        hand_to_bench(my_field)
    
    elif choices[index] == "進化する":
        evolve(my_field)

    elif choices[index] == "サポートカードを使用する":
        use_support(my_field, opponent_field)

    elif choices[index] == "グッズを使用する":
        use_item(my_field, opponent_field)

    elif choices[index] == "攻撃する":
        attack(my_field, opponent_field)

    return None

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
    if can_use_item(field1, field2):
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
    # このターンに逃げた場合は逃げられない
    if field.escaped:
        return False
    # ベンチが空の場合は逃げられない
    if len(field.bench.get_bench_pokemon()) == 0:
        return False
    # 逃げエネ <= エネルギーの合計 + 逃げエネ軽減カードの効果
    total_energy = sum([value for value in field.battle.get_battle_pokemon().energy.values()])
    escape_reduction = field.battle.escape_energy["ス"]
    if field.battle.get_battle_pokemon().convertedRetreatCost <= total_energy + escape_reduction:
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
    pokemon_names = [field.battle.get_battle_pokemon().name] + [pokemon.name for pokemon in field.bench.get_bench_pokemon()]
    for card in field.hand.get_hand():
        if isinstance(card, PokemonCard) and card.evolvesFrom in pokemon_names:
            # このターンに手札から出していないかつ進化していないポケモンがいる場合は進化できる
            for pokemon in [field.battle.get_battle_pokemon()] + field.bench.get_bench_pokemon():
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


def can_use_item(field1, field2):
    for card in field1.hand.get_hand():
        if isinstance(card, ItemCard) and card.check_available(field1, field2):
            return True
    return False

def can_use_ability(field):
    for pokemon in [field.battle.get_battle_pokemon()] + field.bench.get_bench_pokemon():
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
    for attack in field.battle.get_battle_pokemon().attacks:
        # 必要なエネルギーコストをコピーして計算用に保持
        required_cost = attack['cost'].copy()
        available_energy = field.battle.get_battle_pokemon().energy.copy()

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