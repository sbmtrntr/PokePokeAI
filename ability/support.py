from utils.card import SupportCard

# 博士の研究
class ProfessorResearch(SupportCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)

    def check_available(self, field1, field2):
        """
        使用可能かどうかを判定する。
        field1: 自分のフィールド
        field2: 相手のフィールド（使用条件に関係ないが統一性のため引数に含む）
        """
        return field1.stock.get_remaining_cards() > 0

    def __call__(self, field1, field2):
        """
        博士の研究の効果を実行する。
        field1: 自分のフィールド
        field2: 相手のフィールド
        """
        # 山札からカードを2枚ドロー（山札の残りが2枚未満の場合はその分だけドロー）
        draw_count = min(2, field1.stock.get_remaining_cards())
        for _ in range(draw_count):
            pokemon = field1.stock.draw_card()
            if pokemon is not None:
                field1.hand.add_card(pokemon)

        print(f"博士の研究を使用しました。山札から{draw_count}枚のカードを引きました。")


# エリカ
class Erika(SupportCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)

    def check_available(self, field1, field2):
        """
        使用可能かどうかを判定する。
        field1: 自分のフィールド
        field2: 相手のフィールド（効果に関係ないが統一性のため引数に含む）
        """
        # 自分のバトル場とベンチに草タイプのポケモンがいるかチェック
        for pokemon in [field1.battle_field.get_battle_pokemon(), *field1.bench.get_bench_pokemon()]:
            if pokemon.type == "草" and pokemon.hp != pokemon.max_hp:
                return True
        return False

    def __call__(self, field1, field2):
        """
        エリカの効果を実行する。
        field1: 自分のフィールド
        field2: 相手のフィールド（効果に関係ないが統一性のため引数に含む）
        """
        # 回復対象の草タイプポケモンを収集
        eligible_pokemon = {}

        # バトル場
        battle_pokemon = field1.battle_field.get_battle_pokemon()
        if battle_pokemon.type == "草" and battle_pokemon.hp != battle_pokemon.max_hp:
            eligible_pokemon["バトルポケモン"] = battle_pokemon

        # ベンチポケモン
        for i, bench_pokemon in enumerate(field1.bench.get_bench_pokemon()):
            if bench_pokemon.type == "草" and bench_pokemon.hp != bench_pokemon.max_hp:
                eligible_pokemon[f"ベンチポケモン{i+1}"] = bench_pokemon

        # 回復対象を選択
        print("どのポケモンを回復しますか？")
        for index, (key, pokemon) in enumerate(eligible_pokemon.items(), 1):
            print(f"{index}: {key} ({pokemon.name}, HP: {pokemon.hp}/{pokemon.max_hp})")

        choice = input("番号を選んでください: ")
        if not choice.isdigit() or not 1 <= int(choice) <= len(eligible_pokemon):
            print("無効な選択です。")
            return

        selected_pokemon = list(eligible_pokemon.values())[int(choice) - 1]

        # HPを50回復（最大HPを超えないように調整）
        heal_amount = 50
        selected_pokemon.hp = min(selected_pokemon.hp + heal_amount, selected_pokemon.max_hp)
        print(f"{selected_pokemon.name}のHPを{heal_amount}回復しました！")

# ナツメ
class Natsume(SupportCard):
    def __init__(self, name, text):
        super().__init__(name=name, text=text)

    def check_available(self, field1, field2):
        """ナツメが使用可能かを判定する（相手のベンチが1匹以上必要）"""
        return len(field2.bench.get_bench_pokemon()) > 0

    def __call__(self, field1, field2):
        print("ナツメを使用します。相手のバトル場とベンチを入れ替えます。")
        
        # 相手のバトル場のポケモン
        battle_pokemon = field2.battle_field.get_battle_pokemon()

        # 相手のベンチポケモンを選択
        bench_pokemon_list = field2.bench.get_bench_pokemon()
        print("相手のベンチポケモン:")
        for i, pokemon in enumerate(bench_pokemon_list):
            print(f"{i + 1}: {pokemon.name}")

        # 入れ替えるポケモンを選択
        while True:
            user_input = input("入れ替えるポケモンの番号を選んでください: ")
            if not user_input.isdigit():
                print("無効な選択です。もう一度入力してください。")
                continue
            index = int(user_input) - 1
            if 0 <= index < len(bench_pokemon_list):
                break
            print("無効な選択です。もう一度入力してください。")

        # ベンチポケモンを取得
        selected_bench_pokemon = bench_pokemon_list[index]

        # 入れ替え処理
        field2.battle_field.set_battle_pokemon(selected_bench_pokemon)
        field2.bench.get_bench_pokemon()[index] = battle_pokemon

        print(f"{battle_pokemon.name} と {selected_bench_pokemon.name} を入れ替えました。")
        return