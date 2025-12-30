"""
ttt_lib.py - 井字棋遊戲邏輯模組（L3 版本）

此版本目的：
- 提供 GameState 管理棋盤狀態
- 實作 set_move() / is_cell_empty()
- 實作 check_winner() 判斷勝負
- 實作 is_draw() 判斷平手
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
        若該格不空或遊戲已結束，則不動作。
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
    參數：
        board: 2D list，如 [["X","",""],["","O",""],...]
    回傳：
        "X" 或 "O" 表示某一方獲勝
        None 表示尚未分出勝負
    """
    size = len(board)

    # 檢查每一列
    for r in range(size):
        first = board[r][0]
        if first != "" and all(board[r][c] == first for c in range(size)):
            return first

    # 檢查每一行
    for c in range(size):
        first = board[0][c]
        if first != "" and all(board[r][c] == first for r in range(size)):
            return first

    # 檢查主對角線
    first = board[0][0]
    if first != "" and all(board[i][i] == first for i in range(size)):
        return first

    # 檢查反對角線
    first = board[0][size - 1]
    if first != "" and all(board[i][size - 1 - i] == first for i in range(size)):
        return first

    # 沒人贏
    return None


def is_draw(board):
    """
    檢查是否平手：
    - 沒有任何一方獲勝，且
    - 棋盤上已沒有空格
    回傳：
        True  -> 平手
        False -> 尚未平手
    """
    # 有人贏就不是平手
    if check_winner(board) is not None:
        return False

    # 只要還有空格，就不是平手
    for row in board:
        for cell in row:
            if cell == "":
                return False

    return True


# 選擇性：簡單自我測試
if __name__ == "__main__":
    gs = GameState(3)
    gs.set_move(0, 0, "X")
    gs.set_move(0, 1, "X")
    gs.set_move(0, 2, "X")
    print("Winner (預期 X):", check_winner(gs.board))
    print("Is draw (預期 False):", is_draw(gs.board))
