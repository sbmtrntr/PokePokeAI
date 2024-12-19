import logging
import time
from ability import *
from movement import *
from field import Field
from choice import Choice
from utils.coin_toss import do_coin_toss

# logging.basicConfig(
#     filename=f"log/{time.strftime('%Y%m%d-%H%M%S')}.log",
#     level=print,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )


def main(Player1_field, Player2_field):
    print("\n対戦よろしくお願いします")

    # 先行後攻決め
    if do_coin_toss() == "表":
        first_turn = "Player1"
        print("Player1が先行です")
    else:
        first_turn = "Player2"
        print("Player2が先行です")

    turn = 0

    # ゲーム開始
    while True:

        turn += 1
        print(f"\n---{turn}ターン目---")

        if (turn % 2 == 1) == (first_turn == "Player1"):
            print("Player1のターンです")
            
            Player1_field.reset() # 前回の効果をリセット

            # エネルギーを生成
            if not turn == 1:
                Player1_field.energy_zone.generate_energy()

            while True:
                Player1_field.display_field()
                Player2_field.display_field()
                # 選択肢を出力
                choice = Choice(Player1_field)
                choices = choice.display_choice()
                # 選択肢から行動を選択
                index = int(input("上記から行動を選択してください: ")) - 1
                if choices[index] == "ターンを終了": 
                    break

                elif choices[index] == "降参": 
                    exit(print("Player1の負けです"))
                
                elif choices[index] == "エネルギーをつける":
                    Player1_field = attach_energy(Player1_field)

                elif choices[index] == "逃げる":
                    Player1_field = escape(Player1_field)

                elif choices[index] == "たねポケモンをベンチに出す":
                    Player1_field = hand_to_bench(Player1_field)

                # elif choices[index] == "サポートカードを使用する":
                #     Player1_field, Player2_field = use_support(Player1_field, Player2_field)

                # elif choices[index] == "グッズを使用する":
                #     Player1_field, Player2_field = use_item(Player1_field, Player2_field)

                # elif choices[index] == "特性を使用する":
                #     Player1_field, Player2_field = use_ability(Player1_field, Player2_field)

                # elif choices[index] == "攻撃する":
                #     Player1_field, Player2_field = attack(Player1_field, Player2_field)
                else:
                    print("無効な選択です")
            
            if Player1_field.point == 3:
                print("Player1の勝利です")
                break

        else:
            print("Player2のターンです")
            Player2_field.reset()
            # エネルギーを生成
            if not turn == 1:
                Player2_field.energy_zone.generate_energy()

            while True:
                Player2_field.display_field()
                Player1_field.display_field()
                # 選択肢を出力
                choice = Choice(Player2_field)
                choices = choice.display_choice()
                # 選択肢から行動を選択
                index = int(input("上記から行動を選択してください: ")) - 1
                if choices[index] == "ターンを終了": 
                    break

                elif choices[index] == "降参": 
                    exit(print("Player2の負けです"))
                
                elif choices[index] == "エネルギーをつける":
                    Player2_field = attach_energy(Player2_field)

                elif choices[index] == "逃げる":
                    Player2_field = escape(Player2_field)

                elif choices[index] == "たねポケモンをベンチに出す":
                    Player2_field = hand_to_bench(Player2_field)

                # elif choices[index] == "サポートカードを使用する":
                #     Player1_field, Player2_field = use_support(Player1_field, Player2_field)

                # elif choices[index] == "グッズを使用する":
                #     Player1_field, Player2_field = use_item(Player1_field, Player2_field)

                # elif choices[index] == "特性を使用する":
                #     Player1_field, Player2_field = use_ability(Player1_field, Player2_field)

                # elif choices[index] == "攻撃する":
                #     Player1_field, Player2_field = attack(Player1_field, Player2_field)
                else:
                    print("無効な選択です")
            
            if Player2_field.point == 3:
                print("Player2の勝利です")
                break

        
    print("\n対戦ありがとうございました")

if __name__ == "__main__":
    # Player1とPlayer2のフィールドを作成
    Player1_field = Field(player_name="Player1", deck_name="フシギバナEX", energy_type=["草"])
    Player2_field = Field(player_name="Player2", deck_name="リザードンEX", energy_type=["炎"])
    main(Player1_field, Player2_field)
