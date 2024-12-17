import random
from ability import *
from movement import *
from field import Field

# コイントス
def coin_toss():
    return random.choice(["表", "裏"])

def main():
    print("対戦よろしくお願いします")
    
    my_point = 0
    opponent_point = 0

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

        player_field.display_field()
        opponent_field.display_field()

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
    # プレイヤーと相手のフィールドを作成
    player_field = Field(player_name="自分", deck_name="フシギバナEX", energy_type=["草"])
    opponent_field = Field(player_name="相手", deck_name="リザードンEX", energy_type=["炎"])
    main()