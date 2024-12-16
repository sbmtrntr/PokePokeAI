import random
from function import *

# 自分のデッキ（フシギバナex）
my_deck = ["フシギダネ", "フシギダネ", "フシギソウ", "フシギソウ", "フシギバナex", "フシギバナex", "タマタマ", "タマタマ", "ナッシーex", "ナッシーex", 
           "エリカ", "エリカ", "きずぐすり", "きずぐすり", "スピーダー", "スピーダー", "モンスターボール", "モンスターボール", "博士の研究", "博士の研究"]

# 相手のデッキ（リザードンex）
opponent_deck = ["ヒトカゲ", "ヒトカゲ", "リザード", "リザード", "リザードンex", "リザードンex", "ガーディ", "ウインディ", "ファイヤーex", "ファイヤーex", 
                 "ナツメ", "ナツメ", "きずぐすり", "きずぐすり", "スピーダー", "スピーダー", "モンスターボール", "モンスターボール", "博士の研究", "博士の研究"]

# カードのステータスが保存されたJSONファイルのパス
INPUT_FILE = "statics/cards/status.json"

def main():
    print("対戦よろしくお願いします")

    # カードデータをロード
    all_cards = load_cards_status(INPUT_FILE)
    
    # デッキ情報を取得
    my_deck_info = get_card_info(my_deck, all_cards)
    opponent_deck_info = get_card_info(opponent_deck, all_cards)

    # 初期手札を取得
    my_hand = []
    opponent_hand = []
    get_initial_hand(my_hand, my_deck_info)
    get_initial_hand(opponent_hand, opponent_deck_info)

    debug_print(my_hand, my_deck_info)
    print("---")
    debug_print(opponent_hand, opponent_deck_info)


if __name__ == "__main__":
    main()
