from game import Game, Player, Move
from myGame import MyGame
from copy import deepcopy
from math import inf
from typing import Tuple
from tqdm import tqdm
import numpy as np

class MinMax(Player):
  def __init__(self, player_id: int, depth=2) -> None:
    super().__init__()
    self.player_id = player_id
    self.opponent_id = 1 if player_id == 0 else 0
    self.depth = depth

  def evaluate(self, game: 'MyGame'):
    winner = game.check_winner()
    if winner == self.player_id:
      return 10
    elif winner == self.opponent_id:
      return -10
    else:
      longest_seq_player = game.count_longest_seq(self.player_id)
      longest_seq_opponent = game.count_longest_seq(self.opponent_id)
      return longest_seq_player - longest_seq_opponent


  def minimax(self, game: 'Game', depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
    if depth == 0 or game.check_winner() != -1:
      return self.evaluate(game)

    if maximizing_player:
      max_eval = -inf
      possible_moves = game.possible_moves(self.player_id)

      for m in possible_moves:
        new_game = deepcopy(game)
        new_game.move(m[0], m[1], self.player_id)
        new_game.current_player_idx = 1 - new_game.current_player_idx
        score = self.minimax(new_game, depth - 1, alpha, beta, False)
        max_eval = max(max_eval, score)
        alpha = max(alpha, score)
        if beta <= alpha:
          break
      return max_eval
    else:
      min_eval = inf
      possible_moves = game.possible_moves(self.player_id)

      for m in possible_moves:
        new_game = deepcopy(game)
        new_game.move(m[0], m[1], self.player_id)
        new_game.current_player_idx = 1 - new_game.current_player_idx
        score = self.minimax(new_game, depth - 1, alpha, beta, True)
        min_eval = min(min_eval, score)
        beta = min(beta, score)
        if beta <= alpha:
          break
      return min_eval   


  def make_move(self, game: 'Game') -> Tuple[Tuple[int, int], Move]:

    game = MyGame.from_game(game)

    best_score = -inf
    best_move = None
    possible_moves = game.possible_moves(self.player_id)

    for m in possible_moves:
      new_game = deepcopy(game)
      new_game.move(m[0], m[1], self.player_id)
      new_game.current_player_idx = 1 - new_game.current_player_idx
      score = self.minimax(new_game, self.depth - 1, -inf, inf, False)

      if score > best_score:
        best_score = score
        best_move = m

    from_pos, move = best_move
    from_pos = from_pos[::-1]
    return from_pos, move