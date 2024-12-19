# エネルギーをつける
def attach_energy(field):
    print("どのポケモンにエネルギーをつけますか？")
    pokemon_list = [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon()
    for i, pokemon in enumerate(pokemon_list):
        print(f"{i+1}. {pokemon.name}")
    index = int(input("選択肢からポケモンを選択してください: ")) - 1
    field.energy_zone.attach_energy(pokemon_list[index])
    return field

# 逃げる
def escape(field):
    print("どのポケモンと入れ替えますか？")
    for i, pokemon in enumerate(field.bench.get_bench_pokemon()):
        print(f"{i+1}. {pokemon.name}")
    index = int(input("ポケモンの番号を入力してください: ")) - 1
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
    index = int(input("選択肢からポケモンを選択してください: ")) - 1
    field.bench.add_pokemon(pokemon_list[index])
    field.hand.remove_card(pokemon_list[index])
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
