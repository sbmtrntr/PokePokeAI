import os
import platform
from utils.choice.movement import *
from utils.board.field import Field
from utils.choice.choice import choice_action
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
    if Player1_field.battle.get_battle_pokemon() == None:
        print("Player2の勝利です")
        return True
    if Player2_field.battle.get_battle_pokemon() == None:
        print("Player1の勝利です")
        return True
    return False

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
                clear_console()
                print(f"\n---{turn}ターン目---")
                print(f"\n{Player1_field.player_name}のターンです")
                Player2_field.display_as_opponent_field()
                Player1_field.display_as_my_field()
                choice_action(Player1_field, Player2_field, turn)
                if Player1_field.attacked or Player1_field.turn_end:
                    break

        else:
            Player2_field.reset_turn()
            # エネルギーを生成
            if not turn == 1:
                Player2_field.energy_zone.generate_energy()
            while True:
                clear_console()
                print(f"\n---{turn}ターン目---")
                print(f"\n{Player2_field.player_name}のターンです")
                Player1_field.display_as_opponent_field()
                Player2_field.display_as_my_field()
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
