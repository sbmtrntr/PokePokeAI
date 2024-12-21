class PokemonFrame:
        def __init__(self, width=20, height=6):
            self.width = width
            self.height = height
            self.content = [" " * self.width] * self.height  # 空の枠を作成

        def set_content(self, content_lines):
            """枠内に表示する内容を設定"""
            for i, line in enumerate(content_lines):
                if i < self.height:
                    # 内容を中央揃えにして収める
                    self.content[i] = line.center(self.width)

        def get_lines(self):
            """枠の内容をリストで返す"""
            lines = [f"+{'-' * self.width}+"]
            for line in self.content:
                lines.append(f"|{line}|")
            lines.append(f"+{'-' * self.width}+")
            return lines


class Board:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def display_board(self):
        """相手と自分の盤面を表示"""
        MAX_BENCH_SIZE = 3
        frame_width = 20
        divider = "-" * (frame_width * MAX_BENCH_SIZE + 2)

        # フレーム生成
        def create_frames(pokemon_list, max_size):
            frames = []
            for pokemon in pokemon_list:
                frame = PokemonFrame(width=frame_width)
                frame.set_content(pokemon.display_card())
                frames.append(frame)
            while len(frames) < max_size:
                frames.append(PokemonFrame(width=frame_width))  # 空フレーム
            return frames

        # ベンチポケモンフレーム
        my_bench_frames = create_frames(self.field1.bench.get_bench_pokemon(), MAX_BENCH_SIZE)
        opponent_bench_frames = create_frames(self.field2.bench.get_bench_pokemon(), MAX_BENCH_SIZE)

        # バトルポケモンフレーム
        my_battle_frame = PokemonFrame(width=frame_width)
        my_battle_frame.set_content(self.field1.battle.get_battle_pokemon().display_card())
        opponent_battle_frame = PokemonFrame(width=frame_width)
        opponent_battle_frame.set_content(self.field2.battle.get_battle_pokemon().display_card())

        # 相手の盤面表示
        print("\n相手のベンチポケモン:")
        for row in zip(*(frame.get_lines() for frame in opponent_bench_frames)):
            print("".join(row))

        print("\n相手のバトルポケモン:")
        middle_padding = (MAX_BENCH_SIZE - 1) * frame_width // 2
        for line in opponent_battle_frame.get_lines():
            print(" " * middle_padding + line)

        # 区切り線
        print("\n" + divider)

        # 自分の盤面表示
        print("\n自分のバトルポケモン:")
        for line in my_battle_frame.get_lines():
            print(" " * middle_padding + line)

        print("\n自分のベンチポケモン:")
        for row in zip(*(frame.get_lines() for frame in my_bench_frames)):
            print("".join(row))

        # 自分の手札
        print("\n自分の手札:")
        for card in self.field1.hand.get_hand_pokemon():
            print(f"[{card['name']}] ", end="")
        print("\n")