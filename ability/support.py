# 博士の研究
def professor_research(hand, stock):
    if stock.remaining_cards() >= 2:
        for _ in range(2):
            hand.add_card(stock)
    elif stock.remaining_cards() == 1:
        hand.add_card(stock)
    else:
        print("山札にカードがありません。")
    return hand, stock

# エリカ
def erika(pokemon):
    pokemon.hp = min(pokemon.hp + 50, pokemon.max_hp)
    print(f"{pokemon.name}のHPが50回復")
    return pokemon