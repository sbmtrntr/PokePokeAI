from ability import *
from utils.card.card import *

# エネルギーをつける
def attach_energy(field):
    # バトル場
    eligible_pokemon = {}
    battle_pokemon = field.battle.get_battle_pokemon()
    eligible_pokemon["バトル場"] = battle_pokemon

    # ベンチポケモン
    for i, bench_pokemon in enumerate(field.bench.get_bench_pokemon()):
        eligible_pokemon[f"ベンチ{i+1}"] = bench_pokemon
    print("どのポケモンにエネルギーをつけますか？")
    for i, (key, pokemon) in enumerate(eligible_pokemon.items(), 1):
        print(f"{i}: {key} {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return 
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(eligible_pokemon):
            break
        print("無効な入力です。もう一度入力してください")
    selected_pokemon = list(eligible_pokemon.values())[index]
    field.energy_zone.attach_energy(selected_pokemon)
    return 

# 逃げる
def escape(field):
    print("どのポケモンと入れ替えますか？")
    for i, pokemon in enumerate(field.bench.get_bench_pokemon()):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return 
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(field.bench.get_bench_pokemon()):
            break
        print("無効な入力です。もう一度入力してください")
    field.battle.escape_to_bench(field.bench, index)
    return 

# たねポケモンをベンチに出す
def hand_to_bench(field):
    # 手札からたねポケモンを抽出(本当は進化もある)
    pokemon_list = []
    for card in field.hand.get_hand():
        if isinstance(card, PokemonCard) and card.stage == "たね":
            pokemon_list.append(card)
    print("どのポケモンをベンチに出しますか？")
    for i, pokemon in enumerate(pokemon_list):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return 
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(pokemon_list):
            break
        print("無効な入力です。もう一度入力してください")
    field.bench.add_pokemon(pokemon_list[index])
    field.hand.remove_card(pokemon_list[index])
    return 

# 進化する
def evolve(field):
    # バトル場とベンチのポケモンを取得
    pokemon_list = [field.battle.get_battle_pokemon()] + field.bench.get_bench_pokemon()
    # 手札から進化可能なポケモンを抽出
    can_evolve_pokemon = set() #同じポケモンが重複するのを考慮
    for card in field.hand.get_hand():
        if isinstance(card, PokemonCard) and card.evolvesFrom in [pokemon.name for pokemon in pokemon_list]:
            for idx, pokemon in enumerate(pokemon_list):
                if pokemon.name == card.evolvesFrom and not pokemon.has_evolved_this_turn:
                    can_evolve_pokemon.add((idx, pokemon))
    print("どのポケモンを進化しますか？")
    can_evolve_pokemon = list(can_evolve_pokemon)
    for i, (idx, pokemon) in enumerate(can_evolve_pokemon):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return 
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(can_evolve_pokemon):
            break
        print("無効な入力です。もう一度入力してください")
    for card in field.hand.get_hand():
        if isinstance(card, PokemonCard) and card.evolvesFrom == can_evolve_pokemon[index][1].name:
            can_evolve_pokemon[index][1].evolve(card)
            break
    field.hand.remove_card(card)
    return 


# 攻撃する
def attack(field1, field2):
    # 打てる技を表示
    available_attacks = []
    for i, attack in enumerate(field1.battle.get_battle_pokemon().attacks):
        can_attack = False
        # 必要なエネルギーコストをコピーして計算用に保持
        required_cost = attack['cost'].copy()
        available_energy = field1.battle.get_battle_pokemon().energy.copy()

        # 無色エネルギーのコストを取得
        colorless_cost = required_cost.pop("無", 0)

        # 各エネルギータイプのコストをチェック
        for energy_type, energy_cost in required_cost.items():
            if available_energy.get(energy_type, 0) < energy_cost:
                # 必要エネルギーが足りない場合はこの攻撃はできない
                break
            # 必要分を消費する
            available_energy[energy_type] -= energy_cost
            
        # 無色エネルギーの処理（他のエネルギーで代用可能）
        total_available_energy = sum(available_energy.values())
        if total_available_energy >= colorless_cost:
            can_attack = True

        if can_attack:
            available_attacks.append(attack)

    print("どの技を打ちますか？")
    for i, attack in enumerate(available_attacks):
        print(f"{i+1}. {attack['name']}")

    while True:
        user_input = input("技を選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return 
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(available_attacks):
            break
        print("無効な入力です。もう一度入力してください")

    # ダメージ計算
    damage = available_attacks[index]['damage']
    if not damage == 0 and field2.battle.get_battle_pokemon().weakness == field1.battle.get_battle_pokemon().type:
        damage += 20

    # 相手のバトル場のポケモンが攻撃を受ける
    field2.battle.get_battle_pokemon().hp = max(field2.battle.get_battle_pokemon().hp - damage, 0)
    field1.attacked = True

    # 相手のバトル場のポケモンのダメージが0になったら
    if field2.battle.get_battle_pokemon().hp == 0:
        # 相手のバトル場のポケモンがexだったら2ポイント追加
        if field2.battle.get_battle_pokemon().cardRule == "ex":
            field1.point += 2
        else:
            field1.point += 1
        print(f"{field2.battle.get_battle_pokemon().name}が倒れた！")
        if field1.point >= 3:
            exit(print(f"{field1.player_name}の勝利です"))
        else:
            field2.trash.append(field2.battle.get_battle_pokemon())
            field2.battle.set_battle_pokemon(None)
            if len(field2.bench.get_bench_pokemon()) > 0:
                while True:
                    for i, pokemon in enumerate(field2.bench.get_bench_pokemon()):
                        print(f"{i+1}. {pokemon.name}")
                    user_input = input("ベンチからポケモンを選択してください: ")
                    if not user_input.isdigit():  # 数字以外の入力をチェック
                        print("数字を入力してください")
                        continue
                    index = int(user_input) - 1
                    if 0 <= index < len(field2.bench.get_bench_pokemon()):
                        break
                    print("無効な入力です。もう一度入力してください")
                field2.battle.set_battle_pokemon(field2.bench.get_bench_pokemon()[index])
                field2.bench.remove_pokemon(field2.bench.get_bench_pokemon()[index])
            else:
                exit(print(f"{field1.player_name}の勝利です"))

    return

# サポートカードを使用する
def use_support(field1, field2):
    print("どのサポートカードを使用しますか？")
    support_cards = []
    for card in field1.hand.get_hand():
        if isinstance(card, SupportCard) and card.check_available(field1, field2):
            support_cards.append(card)
    for i, card in enumerate(support_cards):
        print(f"{i+1}. {card.name}")
    while True:
        user_input = input("サポートカードを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(support_cards):
            break
        print("無効な入力です。もう一度入力してください")
    support_cards[index](field1, field2)
    field1.hand.remove_card(support_cards[index])
    field1.trash.append(support_cards[index])
    field1.used_support = True
    return

# グッズを使用する
def use_item(field1, field2):
    print("どのグッズを使用しますか？")
    item_cards = []
    for card in field1.hand.get_hand():
        if isinstance(card, ItemCard) and card.check_available(field1, field2):
            item_cards.append(card)
    for i, card in enumerate(item_cards):
        print(f"{i+1}. {card.name}")
    while True:
        user_input = input("グッズを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return 
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(item_cards):
            break
        print("無効な入力です。もう一度入力してください")
    item_cards[index](field1, field2)
    field1.hand.remove_card(item_cards[index])
    field1.trash.append(item_cards[index])
    return