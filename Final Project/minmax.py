from game import Game, Player, Move
from copy import deepcopy
from math import inf
from typing import Tuple
from tqdm import tqdm

class MinMax(Player):
  def __init__(self, player_id: int, depth=2) -> None:
    super().__init__()
    self.player_id = player_id
    self.opponent_id = 1 if player_id == 0 else 0
    self.depth = depth

  def evaluate(self, game: 'Game') -> int:
    if game.check_winner() == self.player_id:
      return self.player_id
    elif game.check_winner() == self.opponent_id:
      return self.opponent_id
    else:
      return -1


  def minimax(self, game: 'Game', depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
    if depth == 0 or game.check_winner() != -1:
      return self.evaluate(game)

    if maximizing_player:
      max_eval = -inf
      possible_moves = game.possible_moves(self.player_id)

      for move in possible_moves:
        new_game = deepcopy(game)
        new_game.move(move[0], move[1], self.player_id)
        score = self.minimax(new_game, depth - 1, alpha, beta, False)
        max_eval = max(max_eval, score)
        alpha = max(alpha, score)
        if beta <= alpha:
          break
      return max_eval
    else:
      min_eval = inf
      possible_moves = game.possible_moves(self.opponent_id)

      for move in possible_moves:
        new_game = deepcopy(game)
        new_game.move(move[0], move[1], self.opponent_id)
        score = self.minimax(new_game, depth - 1, alpha, beta, True)
        min_eval = min(min_eval, score)
        beta = min(beta, score)
        if beta <= alpha:
          break
      return min_eval   


  def make_move(self, game: 'Game') -> Tuple[Tuple[int, int], Move]:
    best_score = -inf
    best_move = None
    possible_moves = game.possible_moves(self.player_id)

    for m in possible_moves:
      new_game = deepcopy(game)
      new_game.move(m[0], m[1], self.player_id)
      score = self.minimax(new_game, self.depth, -inf, inf, False)

      if score > best_score:
        best_score = score
        best_move = m

    from_pos, move = best_move
    return from_pos, move