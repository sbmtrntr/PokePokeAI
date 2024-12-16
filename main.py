import random
from function import *

# カードのステータスが保存されたJSONファイルのパス
INPUT_FILE = "statics/cards/status.json"
# カードデータをロード
all_cards = load_json_file(INPUT_FILE)

# テンプレートデッキJSONファイルのパス
TEMPLATE_DECKS_FILE = "statics/template_decks.json"
# テンプレートデッキをロード
all_template_decks = load_json_file(TEMPLATE_DECKS_FILE)

def main():
    print("対戦よろしくお願いします")
    
    # デッキ情報を取得
    my_deck_info = get_card_info(all_template_decks["VenusaurEX"], all_cards)
    opponent_deck_info = get_card_info(all_template_decks["CharizardEX"], all_cards)

    # 初期手札を取得
    my_hand = []
    opponent_hand = []
    get_initial_hand(my_hand, my_deck_info)
    get_initial_hand(opponent_hand, opponent_deck_info)

    print("---自分---")
    debug_print(my_hand, my_deck_info)
    print("---相手---")
    debug_print(opponent_hand, opponent_deck_info)

    print("対戦ありがとうございました")

if __name__ == "__main__":
    main()
