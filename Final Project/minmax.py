from game import Game, Player, Move
from copy import deepcopy, copy
from typing import Tuple
from random import random
from math import inf
import numpy as np
from tqdm import tqdm

class MinMax:
  def __init__(self, player_id: int) -> None:
    self.player_id = player_id
    self.opponent_id = 1 if player_id == 0 else 0

    def evaluate(self, game: 'Game') -> int:
      if game.check_winner() == self.player_id:
        return 1
      elif game.check_winner() == self.opponent_id:
        return -1
      else:
        return 0
      
