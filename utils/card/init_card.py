import json
import random
from utils.card.card import PokemonCard, SupportCard, ItemCard
from utils.card.ability.support import *
from utils.card.ability.item import *
# JSONファイルをロード
def load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def initialize_cards(deck_name):
    # カードのステータスが保存されたJSONファイルのパス
    CARD_STATUS_FILE = "statics/cards/status.json"
    # カードデータをロード
    all_cards = load_json_file(CARD_STATUS_FILE)

    # テンプレートデッキJSONファイルのパス
    TEMPLATE_DECKS_FILE = "statics/template_decks.json"
    # テンプレートデッキをロード
    all_template_decks = load_json_file(TEMPLATE_DECKS_FILE)

    for deck in all_template_decks:
        if deck["デッキ名"] == deck_name:
            break

    cards = []
    for card_id in deck["カードid"]:
        card = next((c for c in all_cards if c["id"] == card_id), None)
        if card:
            if card.get("category") == "ポケモン":
                cards.append(PokemonCard(
                    name=card.get("name"),
                    cardRule=card.get("cardRule"),
                    evolvesFrom=card.get("evolvesFrom"),
                    stage=card.get("stage"),
                    type=card.get("type"),
                    weakness=card.get("weakness"),
                    hp=card.get("hp"),
                    attacks=card.get("attacks"),
                    convertedRetreatCost=card.get("convertedRetreatCost"),
                    ability=card.get("ability")
                ))
            elif card.get("category") == "トレーナーズ":
                if card.get("subCategory") == "サポート":
                    # 名前でカードを判別して適切なクラスを使用
                    if card.get("name") == "エリカ":
                        cards.append(Erika(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                    elif card.get("name") == "博士の研究":
                        cards.append(ProfessorResearch(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                    elif card.get("name") == "ナツメ":
                        cards.append(Natsume(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                    else:
                        # 汎用的なサポートカードクラスを使う(おそらく使う機会なし)
                        cards.append(SupportCard(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                else:
                    if card.get("name") == "モンスターボール":
                        cards.append(Monsterball(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                    elif card.get("name") == "スピーダー":
                        cards.append(Speeder(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                    elif card.get("name") == "きずぐすり":
                        cards.append(Potion(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
                    else:
                        # 汎用的なグッズカードクラスを使う(おそらく使う機会なし)
                        cards.append(ItemCard(
                            name=card.get("name"),
                            text=card.get("text")
                        ))
        else:
            print(f"Warning: Card '{card_id}' not found in the dataset.")
    
    random.shuffle(cards)
    return cards