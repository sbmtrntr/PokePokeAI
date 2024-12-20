import os
import platform
from ability import *
from utils.movement import *
from utils.field import Field
from utils.choice import display_choice
from utils.coin_toss import do_coin_toss

def clear_console():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def check_game_over(Player1_field, Player2_field):
    if Player1_field.point >= 3:
        print("Player1の勝利です")
        return True
    if Player2_field.point >= 3:
        print("Player2の勝利です")
        return True
    if Player1_field.battle_field.get_battle_pokemon() == None:
        print("Player2の勝利です")
        return True
    if Player2_field.battle_field.get_battle_pokemon() == None:
        print("Player1の勝利です")
        return True
    return False

def choice_action(my_field, opponent_field, turn):
    clear_console()
    print(f"{my_field.player_name}のターンです")
    opponent_field.display_as_opponent_field()
    my_field.display_as_my_field()
    choices = display_choice(my_field, turn)
    while True:
        user_input = input("行動を選択してください: ")
        if not user_input.isdigit():  # 数字以外の入力をチェック
            print("数字を入力してください")
            continue
        index = int(user_input) - 1
        if 0 <= index < len(choices):
            break
        print("無効な入力です。もう一度入力してください")
    
    if choices[index] == "ターンを終了": 
        my_field.turn_end = True

    elif choices[index] == "降参": 
        user_input = input("本当に降参しますか？(y/n): ")
        if user_input == "y":
            exit(print(f"{my_field.player_name}の負けです"))

    
    elif choices[index] == "エネルギーをつける":
        my_field = attach_energy(my_field)

    elif choices[index] == "逃げる":
        my_field = escape(my_field)

    elif choices[index] == "たねポケモンをベンチに出す":
        my_field = hand_to_bench(my_field)
    
    elif choices[index] == "進化する":
        my_field = evolve(my_field)

    # elif choices[index] == "サポートカードを使用する":
    #     Player1_field, Player2_field = use_support(Player1_field, Player2_field)

    # elif choices[index] == "グッズを使用する":
    #     Player1_field, Player2_field = use_item(Player1_field, Player2_field)

    # elif choices[index] == "特性を使用する":
    #     Player1_field, Player2_field = use_ability(Player1_field, Player2_field)

    elif choices[index] == "攻撃する":
        my_field, opponent_field = attack(my_field, opponent_field)

    return None

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
            Player1_field.reset_turn()
            # エネルギーを生成
            if not turn == 1:
                Player1_field.energy_zone.generate_energy()
            while True:
                choice_action(Player1_field, Player2_field, turn)
                if Player1_field.attacked or Player1_field.turn_end:
                    break

        else:
            Player2_field.reset_turn()
            # エネルギーを生成
            if not turn == 1:
                Player2_field.energy_zone.generate_energy()
            while True:
                choice_action(Player2_field, Player1_field, turn)
                if Player2_field.attacked or Player2_field.turn_end:
                    break
        
        if check_game_over(Player1_field, Player2_field):
            break
        
    print("\n対戦ありがとうございました")

if __name__ == "__main__":
    # Player1とPlayer2のフィールドを作成
    Player1_field = Field(player_name="Player1", deck_name="フシギバナEX", energy_type=["草"])
    Player2_field = Field(player_name="Player2", deck_name="リザードンEX", energy_type=["炎"])
    main(Player1_field, Player2_field)
