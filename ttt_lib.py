"""
ttt_lib.py - 井字棋遊戲邏輯的介面草稿（L2 版本）

此版本目的：
- 仍以「介面設計」為主
- 但已經實作基本的棋盤操作（落子、檢查是否為空格）
- 勝負判斷與平手判斷仍先保留為簡化版
"""

class GameState:
    def __init__(self, size=3):
        # 建立 size x size 棋盤，預設為空字串
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.game_over = False

    def is_cell_empty(self, row, col) -> bool:
        """檢查指定格子是否為空"""
        return self.board[row][col] == ""

    def set_move(self, row, col, player):
        """
        在 (row, col) 放入指定玩家的棋子（"X" 或 "O"）。
        這裡不檢查玩家是否合法，只單純寫入。
        """
        if self.is_cell_empty(row, col) and not self.game_over:
            self.board[row][col] = player

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self):
        self.game_over = True


def check_winner(board):
    """
    檢查是否有人獲勝。
    L2 版本仍先回傳 None（表示尚未判斷）。
    未來版本會實作列、行與對角線判斷。
    """
    return None


def is_draw(board):
    """
    檢查是否平手。
    L2 版本仍先回傳 False（永遠不平手）。
    未來版本會依據棋盤是否填滿且無勝負來判斷。
    """
    return False
