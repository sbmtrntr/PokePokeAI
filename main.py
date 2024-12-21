from utils.board import Board, Field
from utils.choice import choice_action
from utils.coin_toss import do_coin_toss


def main(Player1_field, Player2_field):

    print("\n対戦よろしくお願いします")

    # 先行後攻決め
    if do_coin_toss() == "表":
        first_turn = "Player1"
        print("Player1が先行です")
    else:
        first_turn = "Player2"
        print("Player2が先行です")

    turn = [0]
    board = Board(Player1_field, Player2_field, turn, first_turn)

    # 実際はここでたねポケモンを出す処理が必要

    # ゲーム開始
    while True:
        turn[0] += 1

        # Player1のターン
        if (turn[0] % 2 == 1) == (first_turn == "Player1"):
            Player1_field.reset_turn()
            # エネルギーを生成
            if not turn[0] == 1:
                Player1_field.energy_zone.generate_energy()
            while True:
                board.display_board()
                choice_action(Player1_field, Player2_field, turn)
                if Player1_field.attacked or Player1_field.turn_end:
                    break

        # Player2のターン
        else:
            Player2_field.reset_turn()
            # エネルギーを生成
            if not turn[0] == 1:
                Player2_field.energy_zone.generate_energy()
            while True:
                board.display_board()
                choice_action(Player2_field, Player1_field, turn)
                if Player2_field.attacked or Player2_field.turn_end:
                    break
        
        if Player1_field.point >= 3 or Player2_field.point >= 3:
            break
        
    print("\n対戦ありがとうございました")

if __name__ == "__main__":
    # Player1とPlayer2のフィールドを作成
    Player1_field = Field(player_name="Player1", deck_name="フシギバナEX", energy_type=["草"])
    Player2_field = Field(player_name="Player2", deck_name="リザードンEX", energy_type=["炎"])
    main(Player1_field, Player2_field)
