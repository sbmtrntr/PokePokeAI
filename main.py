import random
from ability import *
from field import Field
from choice import Choice

# コイントス
def do_coin_toss():
    coin_toss = random.choice(["表", "裏"])
    print("コイントス: ", coin_toss)
    return coin_toss

def main():
    print("対戦よろしくお願いします")

    # 先行後攻決め
    if do_coin_toss() == "表":
        first_turn = "自分"
        print("自分が先行です")
    else:
        first_turn = "相手"
        print("相手が先行です")

    turn = 0

    # ゲーム開始
    while True:

        turn += 1
        print(f"\n---{turn}ターン目---")

        opponent_field.display_field()
        player_field.display_field()

        if (turn % 2 == 1) == (first_turn == "自分"):
            print("自分のターンです")
            # エネルギーを生成
            if not turn == 1:
                player_field.energy_zone.generate_energy()

            while True:
                # 選択肢を出力
                choice = Choice(player_field)
                choice.display_choice()
                # 選択肢から行動を選択
                index = int(input("選択肢から行動を選択してください: ")) - 1
                if index == 0: break
                elif index == 1: exit(print("自分の負けです"))
                elif index == len(choice.choices) - 1: # 攻撃
                    my_point += choice.select_choice(index)
                    break 
                else: choice.select_choice(index, player_field)

        else:
            print("相手のターンです")
            if not turn == 1:
                player_field.energy_zone.generate_energy()

            while True:
                # 選択肢を出力
                choice = Choice(player_field)
                choice.display_choice()
                # 選択肢から行動を選択
                index = int(input("選択肢から行動を選択してください: ")) - 1
                if index == 0: break
                elif index == 1: exit(print("自分の負けです"))
                elif index == len(choice.choices) - 1: break # 攻撃
                else: choice.select_choice(index)

        if my_point == 3:
            print("自分の勝利です")
            break
        elif opponent_point == 3:
            print("相手の勝利です")
            break
            
        
    print("対戦ありがとうございました")

if __name__ == "__main__":
    # プレイヤーと相手のフィールドを作成
    player_field = Field(player_name="自分", deck_name="フシギバナEX", energy_type=["草"])
    opponent_field = Field(player_name="相手", deck_name="リザードンEX", energy_type=["炎"])
    my_point = 0
    opponent_point = 0
    main()
