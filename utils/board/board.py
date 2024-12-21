import os
import platform
import unicodedata

class PokemonFrame:
    def __init__(self, width=30, height=7):
        self.width = width
        self.height = height
        self.content = [" " * self.width] * self.height  # 空の枠を作成

    def set_content(self, pokemon):
        self.content = []
        WIDTH = self.width

        # 名前、HP、タイプを表示
        self.content.append(f" {pokemon.name}({pokemon.type})  HP:{pokemon.hp}/{pokemon.max_hp} ")

        self.content.append("")
        # 技の表示
        for attack in pokemon.attacks:
            # 攻撃のエネルギーコストを連結
            energies = ''.join([energy_type * num for energy_type, num in attack["cost"].items()])
            self.content.append(f" {energies:<4} {attack['name']} ({attack['damage']}) ")
        
        if len(pokemon.attacks) == 1:
            self.content.append("")
        self.content.append("")

        # 弱点、逃げエネ、エネルギー表示
        self.content.append(f" エネルギー: {''.join([energy_type * num for energy_type, num in pokemon.energy.items()])}")
        self.content.append(f" 弱点: {pokemon.weakness}       逃げエネ: {pokemon.convertedRetreatCost} ")

    def get_lines(self):
        """枠の内容をリストで返す"""
        lines = [f"+{'-' * self.width}+"]
        for line in self.content:
            cnt = self.count_fullwidth(line)
            padding = " " * (self.width - len(line) - cnt)
            lines.append(f"|{line}{padding}|")
        lines.append(f"+{'-' * self.width}+")
        return lines

    def count_fullwidth(self, text):
        count = 0
        for char in text:
            if unicodedata.east_asian_width(char) in ('F', 'W'):  # 全角文字の判定
                count += 1
        return count

class Board:
    def __init__(self, field1, field2, turn, first_turn):
        self.field1 = field1
        self.field2 = field2
        self.turn = turn
        self.first_turn = first_turn

    def display_board(self):
        def clear_console():
            os.system('cls' if platform.system() == 'Windows' else 'clear')

        clear_console()
        print(f"---{self.turn[0]}ターン目---")

        MAX_BENCH_SIZE = 3
        frame_width = 32
        divider = "-" * (frame_width * MAX_BENCH_SIZE + 8)

        # フレーム生成
        def create_frames(pokemon_list, max_size):
            frames = []
            for pokemon in pokemon_list:
                frame = PokemonFrame(width=frame_width)
                frame.set_content(pokemon)
                frames.append(frame)
            while len(frames) < max_size:
                frames.append(PokemonFrame(width=frame_width))  # 空フレーム
            return frames

        # ベンチポケモンフレーム
        my_bench_frames = create_frames(self.field1.bench.get_bench_pokemon(), MAX_BENCH_SIZE)
        opponent_bench_frames = create_frames(self.field2.bench.get_bench_pokemon(), MAX_BENCH_SIZE)

        # バトルポケモンフレーム
        my_battle_frame = PokemonFrame(width=frame_width)
        my_battle_frame.set_content(self.field1.battle.get_battle_pokemon())
        opponent_battle_frame = PokemonFrame(width=frame_width)
        opponent_battle_frame.set_content(self.field2.battle.get_battle_pokemon())

        # Player2の盤面表示
        # print(f"\nPlayer2 {self.field2.point}ポイント")
        for row in zip(*(frame.get_lines() for frame in opponent_bench_frames)):
            print("".join(row))

        # print("\nPlayer2のバトルポケモン:")
        print()
        middle_padding = (MAX_BENCH_SIZE - 1) * frame_width // 2 + 2
        for line in opponent_battle_frame.get_lines():
            print(" " * middle_padding + line)

        print(f"\nPlayer2")
        print(f"{self.field2.point}ポイント")

        # 区切り線
        print("\n" + divider)

        print("\nPlayer1")
        print(f"{self.field1.point}ポイント")

        # Player1の盤面表示
        for line in my_battle_frame.get_lines():
            print(" " * middle_padding + line)

        # print("\nPlayer1のベンチポケモン:")
        print()
        for row in zip(*(frame.get_lines() for frame in my_bench_frames)):
            print("".join(row))

        # Player1の手札
        if (self.turn[0] % 2 == 1) == (self.first_turn == "Player1"):
            print("\nPlayer1の手札:")
            for card in self.field1.hand.get_hand():
                print(f"[{card.name}] ", end="")
        else:
            print("\nPlayer2の手札:")
            for card in self.field2.hand.get_hand():
                print(f"[{card.name}] ", end="")
        print("\n")
