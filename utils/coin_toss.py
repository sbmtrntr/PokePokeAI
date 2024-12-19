# コイントスだけの贅沢なモジュール
import random
# コイントス
def do_coin_toss():
    coin_toss = random.choice(["表", "裏"])
    print("コイントス: ", coin_toss)
    return coin_toss