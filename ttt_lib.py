"""
ttt_lib.py - 井字棋遊戲邏輯的自訂lib

此版本目的：
- 先定義介面（API）
- 之後才會有（勝負判斷、平手判斷等）
"""

class GameState:
    def __init__(self, size=3):
        # 建立 size x size 棋盤
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.game_over = False

    def is_cell_empty(self, row, col) -> bool:
        
        return True

    def set_move(self, row, col, player):
        
        pass

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self):
        self.game_over = True


def check_winner(board):
    """
    檢查是否有人獲勝。
    """
    return None


def is_draw(board):
    """
    檢查是否平手。
    """
    return False
