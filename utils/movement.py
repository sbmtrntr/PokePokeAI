# エネルギーをつける
def attach_energy(field):
    print("どのポケモンにエネルギーをつけますか？")
    pokemon_list = [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon()
    for i, pokemon in enumerate(pokemon_list):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return field
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(pokemon_list):
            break
        print("無効な入力です。もう一度入力してください")
    field.energy_zone.attach_energy(pokemon_list[index])
    return field

# 逃げる
def escape(field):
    print("どのポケモンと入れ替えますか？")
    for i, pokemon in enumerate(field.bench.get_bench_pokemon()):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return field
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(field.bench.get_bench_pokemon()):
            break
        print("無効な入力です。もう一度入力してください")
    field.battle_field.escape_to_bench(field.bench, index)
    return field

# たねポケモンをベンチに出す
def hand_to_bench(field):
    # 手札からたねポケモンを抽出(本当は進化もある)
    pokemon_list = []
    for card in field.hand.get_hand():
        if card.category == "ポケモン" and card.stage == "たね":
            pokemon_list.append(card)
    print("どのポケモンをベンチに出しますか？")
    for i, pokemon in enumerate(pokemon_list):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return field
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(pokemon_list):
            break
        print("無効な入力です。もう一度入力してください")
    field.bench.add_pokemon(pokemon_list[index])
    field.hand.remove_card(pokemon_list[index])
    return field

# 進化する
def evolve(field):
    # バトル場とベンチのポケモンを取得
    pokemon_list = [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon()
    # 手札から進化可能なポケモンを抽出
    can_evolve_pokemon = set() #同じポケモンが重複するのを考慮
    for card in field.hand.get_hand():
        if card.category == "ポケモン" and card.evolvesFrom in [pokemon.name for pokemon in pokemon_list]:
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
                return field
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(can_evolve_pokemon):
            break
        print("無効な入力です。もう一度入力してください")
    for card in field.hand.get_hand():
        if card.category == "ポケモン" and card.evolvesFrom == can_evolve_pokemon[index][1].name:
            can_evolve_pokemon[index][1].evolve(card)
            break
    field.hand.remove_card(card)
    return field


# 攻撃する
def attack(field1, field2):
    # 打てる技を表示
    available_attacks = []
    for i, attack in enumerate(field1.battle_field.get_battle_pokemon().attacks):
        required_energy = attack['cost'].copy()
        energy_copy = field1.battle_field.get_battle_pokemon().energy.copy() # 元のエネルギー状態を変更しないためコピー
        can_attack = True
        # 各エネルギータイプの条件をチェック
        for energy_type, amount_needed in required_energy.items():
            if energy_type != "無":
                # 特定タイプのエネルギーを消費
                if energy_copy[energy_type] < amount_needed:
                    can_attack = False
                    break
                else:
                    energy_copy[energy_type] -= amount_needed
            else:
                # 無色エネルギーを全体の合計から消費
                total_energy = sum(energy_copy.values())
                if total_energy < amount_needed:
                    can_attack = False
                    break
                else:
                    # 全体から無色エネルギーを消費
                    total_energy -= amount_needed
        if can_attack:
            available_attacks.append(attack)

    print("どの技を打ちますか？")
    for i, attack in enumerate(available_attacks):
        print(f"{i+1}. {attack['name']}")

    while True:
        user_input = input("技を選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return field1, field2
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(available_attacks):
            break
        print("無効な入力です。もう一度入力してください")

    # ダメージ計算
    damage = available_attacks[index]['damage']
    if not damage == 0 and field2.battle_field.get_battle_pokemon().weakness == field1.battle_field.get_battle_pokemon().type:
        damage += 20

    # 相手のバトル場のポケモンが攻撃を受ける
    field2.battle_field.get_battle_pokemon().hp = max(field2.battle_field.get_battle_pokemon().hp - damage, 0)
    field1.attacked = True

    # 相手のバトル場のポケモンのダメージが0になったら
    if field2.battle_field.get_battle_pokemon().hp == 0:
        # 相手のバトル場のポケモンがexだったら2ポイント追加
        if field2.battle_field.get_battle_pokemon().cardRule == "ex":
            field1.point += 2
        else:
            field1.point += 1
        print(f"{field2.battle_field.get_battle_pokemon().name}が倒れた！")
        if field1.point >= 3:
            exit(print(f"{field1.player_name}の勝利です"))
        else:
            field2.trash.append(field2.battle_field.get_battle_pokemon())
            field2.battle_field.set_battle_pokemon(None)
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
                field2.battle_field.set_battle_pokemon(field2.bench.get_bench_pokemon()[index])
                field2.bench.remove_pokemon(field2.bench.get_bench_pokemon()[index])
            else:
                exit(print(f"{field1.player_name}の勝利です"))

    return field1, field2

# # サポートカードを使用する
# def use_support(field1, field2):
#     print("どのサポートカードを使用しますか？")
#     for i, card in enumerate(field.hand.get_hand()):
#         print(f"{i+1}. {card.name}")
#     index = int(input("選択肢からサポートカードを選択してください: ")) - 1
#     support_cards[index].use()

# # グッズを使用する
# def use_item(field1, field2):
#     print("どのグッズを使用しますか？")
#     for i, card in enumerate(field.hand.get_hand()):
#         print(f"{i+1}. {card.name}")
#     index = int(input("選択肢からグッズを選択してください: ")) - 1
#     field.hand.get_hand()[index].use()


# # 特性を使用する
# def use_ability(field1, field2):
#     print("どの特性を使用しますか？")
#     for i, card in enumerate(field.hand.get_hand()):
#         print(f"{i+1}. {card.name}")
#     index = int(input("選択肢から特性を選択してください: ")) - 1
#     field.hand.get_hand()[index].use()

