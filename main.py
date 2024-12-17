import random
from utils.function import *
from utils.ability import *

def main():
    print("対戦よろしくお願いします")

    # 初期手札を取得
    my_hand = get_initial_hand(my_stock)
    opponent_hand = get_initial_hand(opponent_stock)

    print("---自分---")
    debug_print(my_hand, my_stock)
    print("---相手---")
    debug_print(opponent_hand, opponent_stock)
    
    print("対戦ありがとうございました")

if __name__ == "__main__":
    # 山札を取得
    my_stock = get_stock("フシギバナEX")
    opponent_stock = get_stock("リザードンEX")
    main()
