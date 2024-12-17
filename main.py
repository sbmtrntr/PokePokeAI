import random
from utils.function import *
from utils.ability import *

def main():
    print("対戦よろしくお願いします")

    my_point = 0
    opponent_point = 0
    my_next_energy = random.choice(my_energy_type)
    opponent_next_energy = random.choice(opponent_energy_type)

    # 初期手札を取得
    my_hand = get_initial_hand(my_stock)
    opponent_hand = get_initial_hand(opponent_stock)

    print("---自分---")
    debug_print(my_hand, my_stock)
    print("---相手---")
    debug_print(opponent_hand, opponent_stock)

    # 先行後攻決め
    if coin_toss() == "表":
        first_turn = "自分"
        print("自分が先行です")
    else:
        first_turn = "相手"
        print("相手が先行です")

    turn = 0
    # ゲーム開始
    while True:
        if my_point == 3:
            print("自分の勝利です")
            break
        elif opponent_point == 3:
            print("相手の勝利です")
            break

        turn += 1
        print(f"{turn}ターン目")

        if (turn % 2 == 1) == (first_turn == "自分"):
            print("自分のターンです")
            if not turn == 1:
                my_energy = my_next_energy
                my_next_energy = random.choice(my_energy_type)
        else:
            if not turn == 1:
                opponent_energy = opponent_next_energy
                opponent_next_energy = random.choice(opponent_energy_type)
            print("相手のターンです")
            
        
    print("対戦ありがとうございました")

if __name__ == "__main__":
    # 山札を取得
    my_stock, my_energy_type = get_stock("フシギバナEX")
    opponent_stock, opponent_energy_type = get_stock("リザードンEX")
    main()
