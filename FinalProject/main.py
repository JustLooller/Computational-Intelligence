import random
from game import Game, Move, Player
from tqdm import tqdm

from minmax import MinMax
from myGame import MyGame

class RandomPlayer(Player):
    def __init__(self) -> None:
        super().__init__()

    def make_move(self, game: 'MyGame') -> tuple[tuple[int, int], Move]:
        from_pos = (random.randint(0, 4), random.randint(0, 4))
        move = random.choice([Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT])
        return from_pos, move


if __name__ == '__main__':

    wins = 0
    for _ in tqdm(range(10), desc="MinMax vs Random", unit="game"):
        g = Game()
        player1 = MinMax(0, 2)
        player2 = RandomPlayer()
        winner= g.play(player1, player2)
        if winner == 0: wins += 1
    print(f"MinMax player with depth 2 as first player wins: {wins}")
    print(f"Random player as second player wins: {10 - wins}")

    wins = 0
    for _ in tqdm(range(10), desc="Random vs MinMax", unit="game"):
        g = MyGame()
        player1 = RandomPlayer()
        player2 = MinMax(1, 2)
        winner= g.play(player1, player2)
        if winner == 1: wins += 1
    print(f"MinMax player with depth 2 as second player wins: {wins}")
    print(f"Random player as first player wins: {10 - wins}")