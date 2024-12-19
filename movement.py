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
    field.bench.get_bench()[index], field.battle_field.get_battle_pokemon() = field.battle_field.get_battle_pokemon(), field.bench.get_bench()[index]
    return field

# # ベンチに出す
# def hand_to_bench(field):
    
#     print("どのポケモンをベンチに出しますか？")
#     for i, pokemon in enumerate(field.hand.get_hand()):
#         print(f"{i+1}. {pokemon.name}")
#     index = int(input("選択肢からポケモンを選択してください: ")) - 1
#     return hand[index], hand[:index] + hand[index+1:]


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
