import logging
import time
from ability import *
from field import Field
from choice import Choice
from movement import *
from utils.coin_toss import do_coin_toss

# logging.basicConfig(
#     filename=f"log/{time.strftime('%Y%m%d-%H%M%S')}.log",
#     level=print,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )


def main():
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
            Player1_field.initialize_field()
            # エネルギーを生成
            if not turn == 1:
                Player1_field.energy_zone.generate_energy()
            
            Player1_field.display_field()
            Player2_field.display_field()

            while True:
                # 選択肢を出力
                choice = Choice(Player1_field)
                choices = choice.display_choice()
                # 選択肢から行動を選択
                index = int(input("選択肢から行動を選択してください: ")) - 1
                if choices[index] == "ターンを終了": 
                    break

                elif choices[index] == "降参": 
                    exit(print("Player1の負けです"))

                elif choices[index] == "逃げる":
                    Player1_field = escape(Player1_field)

                elif choices[index] == "たねポケモンをベンチに出す":
                    Player1_field = hand_to_bench(Player1_field)

                elif choices[index] == "サポートカードを使用する":
                    Player1_field, Player2_field = use_support(Player1_field, Player2_field)

                elif choices[index] == "グッズを使用する":
                    Player1_field, Player2_field = use_item(Player1_field, Player2_field)

                elif choices[index] == "特性を使用する":
                    Player1_field, Player2_field = use_ability(Player1_field, Player2_field)

                elif choices[index] == "エネルギーをつける":
                    Player1_field = attach_energy(Player1_field)

                elif choices[index] == "攻撃する":
                    Player1_field, Player2_field = attack(Player1_field, Player2_field)
                else:
                    print("無効な選択です")
            
            if Player1_field.point == 3:
                print("Player1の勝利です")
                break

        else:
            print("Player2のターンです")
            Player2_field.initialize_field()
            if not turn == 1:
                Player2_field.energy_zone.generate_energy()

            Player2_field.display_field()
            Player1_field.display_field()

            while True:
                # 選択肢を出力
                choice = Choice(Player1_field)
                choice.display_choice()
                # 選択肢から行動を選択
                index = int(input("選択肢から行動を選択してください: ")) - 1
                if index == 0: break # ターン終了
                elif index == 1: exit(print("Player1の負けです")) # 降参
                elif index == len(choice.choices) - 1: break # 攻撃
                else: choice.select_choice(index) # その他
            
            if Player2_field.point == 3:
                print("Player2の勝利です")
                break
        
    print("\n対戦ありがとうございました")

if __name__ == "__main__":
    # プレイヤーとPlayer2のフィールドを作成
    Player1_field = Field(player_name="Player1", deck_name="フシギバナEX", energy_type=["草"])
    Player2_field = Field(player_name="Player2", deck_name="リザードンEX", energy_type=["炎"])
    try:
        main()
    except Exception as e:
        logging.error(f"エラーが発生しました: {e}")
