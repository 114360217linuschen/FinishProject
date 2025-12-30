"""
ttt_lib.py - 井字棋遊戲邏輯模組（L4 版本）

相較 L3：
- 保留原有 API：check_winner(board) -> "X"/"O"/None（不改）
- 新增 get_winning_cells(board)：
    - 若有人獲勝，回傳該勝利線的座標列表 [(r,c), ...]
    - 若沒人獲勝，回傳 []
用途：
- 讓 UI 可以在獲勝時標示出勝利連線
"""

class GameState:
    def __init__(self, size=3):
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.game_over = False

    def is_cell_empty(self, row, col) -> bool:
        return self.board[row][col] == ""

    def set_move(self, row, col, player):
        """若遊戲未結束且該格為空，則落子。"""
        if self.is_cell_empty(row, col) and not self.game_over:
            self.board[row][col] = player

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self):
        self.game_over = True


def check_winner(board):
    """
    回傳：
      - "X" / "O"：某一方獲勝
      - None：尚未分出勝負
    """
    cells = get_winning_cells(board)
    if not cells:
        return None
    r0, c0 = cells[0]
    return board[r0][c0]


def get_winning_cells(board):
    """
    若有人獲勝，回傳勝利線座標，例如 [(0,0),(0,1),(0,2)]
    若無勝利線，回傳 []
    """
    size = len(board)

    # 列
    for r in range(size):
        first = board[r][0]
        if first != "" and all(board[r][c] == first for c in range(size)):
            return [(r, c) for c in range(size)]

    # 行
    for c in range(size):
        first = board[0][c]
        if first != "" and all(board[r][c] == first for r in range(size)):
            return [(r, c) for r in range(size)]

    # 主對角線
    first = board[0][0]
    if first != "" and all(board[i][i] == first for i in range(size)):
        return [(i, i) for i in range(size)]

    # 反對角線
    first = board[0][size - 1]
    if first != "" and all(board[i][size - 1 - i] == first for i in range(size)):
        return [(i, size - 1 - i) for i in range(size)]

    return []


def is_draw(board):
    """
    平手條件：
    - 沒有任何一方獲勝
    - 棋盤上沒有空格
    """
    if check_winner(board) is not None:
        return False

    for row in board:
        for cell in row:
            if cell == "":
                return False

    return True


if __name__ == "__main__":
    # 簡單自測
    gs = GameState(3)
    gs.set_move(0, 0, "X")
    gs.set_move(0, 1, "X")
    gs.set_move(0, 2, "X")
    print("Winner (預期 X):", check_winner(gs.board))
    print("Winning cells (預期 [(0,0),(0,1),(0,2)]):", get_winning_cells(gs.board))
    print("Is draw (預期 False):", is_draw(gs.board))
