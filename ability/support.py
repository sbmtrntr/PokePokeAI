# 博士の研究
def professor_research(field):
    if field.stock.remaining_cards() >= 2:
        for _ in range(2):
            field.hand.add_card(field.stock)
    elif field.stock.remaining_cards() == 1:
        field.hand.add_card(field.stock)
    else:
        print("山札にカードがありません。")
    return field

# エリカ
def erika(field):
    print("どのポケモンに使用しますか？")
    leaf_type_pokemon = []
    for pokemon in [field.battle_field.get_battle_pokemon()] + field.bench.get_bench_pokemon():
        if pokemon.type == "草":
            leaf_type_pokemon.append(pokemon)

    for i, pokemon in enumerate(leaf_type_pokemon):
        print(f"{i+1}. {pokemon.name}")
    while True:
        user_input = input("ポケモンを選択してください(戻る: q): ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            if user_input == "q":
                return field
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(leaf_type_pokemon):
            break
        print("無効な入力です。もう一度入力してください")
    field.bench.get_bench()[index].hp = min(field.bench.get_bench()[index].hp + 50, field.bench.get_bench()[index].max_hp)
    print(f"{field.bench.get_bench()[index].name}のHPが50回復")
    return field