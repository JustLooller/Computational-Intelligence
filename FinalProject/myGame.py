from game import Game, Move, Player
import numpy as np
from copy import deepcopy


class MyGame(Game):
    def __init__(self) -> None:
      super().__init__()
    
    def move(self, from_pos: tuple[int, int], slide: Move, player_id: int) -> bool:
      '''Perform a move'''
      if player_id > 2:
          return False
      # Oh God, Numpy arrays
      prev_value = deepcopy(self._board[(from_pos[0], from_pos[1])])
      acceptable = self._Game__take((from_pos[0], from_pos[1]), player_id)
      if acceptable:
          acceptable = self._Game__slide((from_pos[0], from_pos[1]), slide)
          if not acceptable:
              self._board[(from_pos[0], from_pos[1])] = deepcopy(prev_value)
      return acceptable

    def possible_moves(self, player_id: int) -> list[tuple[tuple[int, int], Move]]:
      '''Get all possible moves'''
      possible_moves: list[tuple[tuple[int, int], Move]] = []
      CORNERS = [(0, 0), (0, 4), (4, 0), (4, 4)]
      ALL_MOVES = [Move.TOP, Move.BOTTOM, Move.LEFT, Move.RIGHT]
      
      for i in range(len(CORNERS)):
          if i == 0:
              if self._board[CORNERS[i]] == -1 or self._board[CORNERS[i]] == player_id:
                  possible_moves.append((CORNERS[i], Move.RIGHT))
                  possible_moves.append((CORNERS[i], Move.BOTTOM))
          if i == 1:
              if self._board[CORNERS[i]] == -1 or self._board[CORNERS[i]] == player_id:
                  possible_moves.append((CORNERS[i], Move.LEFT))
                  possible_moves.append((CORNERS[i], Move.BOTTOM))
          if i == 2:
              if self._board[CORNERS[i]] == -1 or self._board[CORNERS[i]] == player_id:
                  possible_moves.append((CORNERS[i], Move.RIGHT))
                  possible_moves.append((CORNERS[i], Move.TOP))
          if i == 3:
              if self._board[CORNERS[i]] == -1 or self._board[CORNERS[i]] == player_id:
                  possible_moves.append((CORNERS[i], Move.LEFT))
                  possible_moves.append((CORNERS[i], Move.TOP))

      for i in range(1, self._board.shape[0] - 1):
          if self._board[i, 0] == -1 or self._board[i, 0] == player_id:
              possible_moves.append(((i, 0), Move.RIGHT))
              possible_moves.append(((i, 0), Move.BOTTOM))
              possible_moves.append(((i, 0), Move.TOP))
          if self._board[i, 4] == -1 or self._board[i, 4] == player_id:
              possible_moves.append(((i, 4), Move.LEFT))
              possible_moves.append(((i, 4), Move.BOTTOM))
              possible_moves.append(((i, 4), Move.TOP))
      for i in range(1, self._board.shape[1] - 1):
          if self._board[0, i] == -1 or self._board[0, i] == player_id:
              possible_moves.append(((0, i), Move.BOTTOM))
              possible_moves.append(((0, i), Move.LEFT))
              possible_moves.append(((0, i), Move.RIGHT))
          if self._board[4, i] == -1 or self._board[4, i] == player_id:
              possible_moves.append(((4, i), Move.TOP))
              possible_moves.append(((4, i), Move.LEFT))
              possible_moves.append(((4, i), Move.RIGHT))

      return possible_moves

    def count_longest_seq(self, player_id:int) -> int:
        '''Count the longest sequence of pieces'''
        max_consecutive = max(np.max(np.where(self._board == player_id, 1, 0).sum(axis=0)), np.max(np.where(self._board == player_id, 1, 0).sum(axis=1)))
        princ_diagonal = np.diagonal(self._board)
        sec_diagonal = np.diagonal(np.fliplr(self._board))
        total_max = max(max_consecutive, np.max(np.where(princ_diagonal == player_id, 1, 0).sum(axis=0)), np.max(np.where(sec_diagonal == player_id, 1, 0).sum(axis=0)))
        return total_max

    @staticmethod
    def from_game(game: Game) -> 'MyGame':
        '''Create a new game from an existing game'''
        new_game = MyGame()
        new_game._board = deepcopy(game.get_board())
        new_game.current_player_idx = game.get_current_player()
        return new_game