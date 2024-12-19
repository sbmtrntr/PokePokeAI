# エネルギーをつける
def attach_energy(field):
    print("どのポケモンにエネルギーをつけますか？")
    pokemon_list = [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon()
    for i, pokemon in enumerate(pokemon_list):
        print(f"{i+1}. {pokemon.name}")
    while True:
        index = int(input("ポケモンを選択してください: ")) - 1
        if index >= 0:
            break
        print("入力が空です。もう一度入力してください")
    field.energy_zone.attach_energy(pokemon_list[index])
    return field

# 逃げる
def escape(field):
    print("どのポケモンと入れ替えますか？")
    for i, pokemon in enumerate(field.bench.get_bench_pokemon()):
        print(f"{i+1}. {pokemon.name}")
    while True:
        index = int(input("ポケモンを選択してください: ")) - 1
        if index >= 0:
            break
        print("入力が空です。もう一度入力してください")
    field.battle_field.swap_with_bench(field.bench, index)
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
        index = int(input("ポケモンを選択してください: ")) - 1
        if index >= 0:
            break
        print("入力が空です。もう一度入力してください")
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
        index = int(input("ポケモンを選択してください: ")) - 1
        if index >= 0:
            break
        print("入力が空です。もう一度入力してください")
    for card in field.hand.get_hand():
        if card.category == "ポケモン" and card.evolvesFrom == can_evolve_pokemon[index][1].name:
            can_evolve_pokemon[index][1].evolve(card)
            break
    field.hand.remove_card(card)
    return field

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

# # 攻撃する
# def attack(field1, field2):
#     return fie
