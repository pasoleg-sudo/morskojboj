import random
import string

BOARD_SIZE = 5
SHIP_LENGTHS = [3, 2]


class Board:
    def __init__(self, size: int) -> None:
        self.size = size
        self.ships = set()
        self.hits = set()
        self.misses = set()

    def place_ship_random(self, length: int, rng: random.Random) -> None:
        placed = False
        while not placed:
            horizontal = rng.choice([True, False])
            if horizontal:
                row = rng.randrange(self.size)
                col = rng.randrange(self.size - length + 1)
                coords = {(row, c) for c in range(col, col + length)}
            else:
                row = rng.randrange(self.size - length + 1)
                col = rng.randrange(self.size)
                coords = {(r, col) for r in range(row, row + length)}
            if not coords & self.ships:
                self.ships |= coords
                placed = True

    def receive_shot(self, coord: tuple[int, int]) -> bool:
        if coord in self.ships:
            self.hits.add(coord)
            return True
        self.misses.add(coord)
        return False

    def all_sunk(self) -> bool:
        return self.ships <= self.hits

    def render(self, reveal: bool = False) -> str:
        header = "  " + " ".join(str(i + 1) for i in range(self.size))
        rows = [header]
        for row in range(self.size):
            row_label = string.ascii_uppercase[row]
            cells = []
            for col in range(self.size):
                coord = (row, col)
                if coord in self.hits:
                    cells.append("X")
                elif coord in self.misses:
                    cells.append("·")
                elif reveal and coord in self.ships:
                    cells.append("O")
                else:
                    cells.append("~")
            rows.append(f"{row_label} " + " ".join(cells))
        return "\n".join(rows)


class Game:
    def __init__(self) -> None:
        self.rng = random.Random()
        self.player = Board(BOARD_SIZE)
        self.computer = Board(BOARD_SIZE)
        for length in SHIP_LENGTHS:
            self.player.place_ship_random(length, self.rng)
            self.computer.place_ship_random(length, self.rng)
        self.available_computer_shots = [
            (r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)
        ]
        self.rng.shuffle(self.available_computer_shots)

    def parse_coord(self, raw: str) -> tuple[int, int] | None:
        raw = raw.strip().upper()
        if len(raw) < 2:
            return None
        row_char = raw[0]
        if row_char not in string.ascii_uppercase[: self.player.size]:
            return None
        try:
            col = int(raw[1:]) - 1
        except ValueError:
            return None
        row = string.ascii_uppercase.index(row_char)
        if not (0 <= col < self.player.size):
            return None
        return row, col

    def player_turn(self) -> None:
        while True:
            raw = input("Ваш выстрел (например, A1): ")
            coord = self.parse_coord(raw)
            if coord is None:
                print("Неверный ввод. Используйте формат A1.")
                continue
            if coord in self.computer.hits or coord in self.computer.misses:
                print("Вы уже стреляли сюда.")
                continue
            hit = self.computer.receive_shot(coord)
            print("Попадание!" if hit else "Мимо.")
            break

    def computer_turn(self) -> None:
        coord = self.available_computer_shots.pop()
        hit = self.player.receive_shot(coord)
        row, col = coord
        row_label = string.ascii_uppercase[row]
        print(f"Компьютер стреляет {row_label}{col + 1}: " + ("попадание!" if hit else "мимо."))

    def print_boards(self) -> None:
        print("\nВаше поле:")
        print(self.player.render(reveal=True))
        print("\nПоле компьютера:")
        print(self.computer.render(reveal=False))
        print()

    def run(self) -> None:
        print("Добро пожаловать в Морской бой!")
        while True:
            self.print_boards()
            self.player_turn()
            if self.computer.all_sunk():
                print("Вы победили!")
                break
            self.computer_turn()
            if self.player.all_sunk():
                print("Вы проиграли.")
                break
        print("\nИгра окончена.")
        print("Поле компьютера:")
        print(self.computer.render(reveal=True))


if __name__ == "__main__":
    Game().run()
