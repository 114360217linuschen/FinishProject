"""
ttt_lib.py - 井字棋遊戲邏輯模組（L5 版本）

保留（不破壞前面版本的 API）：
- GameState
- check_winner(board) -> "X"/"O"/None
- is_draw(board) -> bool
- get_winning_cells(board) -> list[(r,c)]

新增（L5）：
- 戰績統計與歷史紀錄（存成 JSON 檔）
  - load_stats() / save_stats(stats)
  - append_history(record) / load_history(limit)
"""

from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime


# ====== 存檔路徑（放在同資料夾）======
BASE_DIR = Path(__file__).resolve().parent
STATS_FILE = BASE_DIR / "ttt_stats.json"
HISTORY_FILE = BASE_DIR / "ttt_history.json"


# ====== 原本的遊戲狀態 ======
class GameState:
    def __init__(self, size=3):
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.game_over = False

    def is_cell_empty(self, row, col) -> bool:
        return self.board[row][col] == ""

    def set_move(self, row, col, player):
        if self.is_cell_empty(row, col) and not self.game_over:
            self.board[row][col] = player

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self):
        self.game_over = True


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


# ====== L5：戰績/歷史存檔 ======

def _read_json_file(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _write_json_file(path: Path, data):
    # 確保寫入時不會亂碼
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def default_stats():
    return {"X": 0, "O": 0, "draw": 0, "total": 0}


def load_stats():
    """
    讀取統計資料：
    回傳 dict: {"X":int, "O":int, "draw":int, "total":int}
    """
    stats = _read_json_file(STATS_FILE, default_stats())
    # 防禦性：缺 key 就補上
    base = default_stats()
    for k in base:
        if k not in stats or not isinstance(stats[k], int):
            stats[k] = base[k]
    return stats


def save_stats(stats: dict):
    """把統計資料寫回檔案"""
    _write_json_file(STATS_FILE, stats)


def update_stats(winner: str | None):
    """
    winner:
      - "X" / "O"：某一方獲勝
      - None：平手
    回傳更新後 stats
    """
    stats = load_stats()
    if winner in ("X", "O"):
        stats[winner] += 1
    else:
        stats["draw"] += 1
    stats["total"] += 1
    save_stats(stats)
    return stats


def append_history(record: dict):
    """
    新增一筆歷史紀錄到 HISTORY_FILE
    record 建議包含：
      - time: ISO string
      - winner: "X"/"O"/"draw"
      - first_player: "X"/"O"
      - moves: int
    """
    history = _read_json_file(HISTORY_FILE, [])
    if not isinstance(history, list):
        history = []
    history.append(record)
    _write_json_file(HISTORY_FILE, history)


def load_history(limit: int = 20):
    """
    讀取最近 limit 筆歷史（新的在最後）
    回傳 list[dict]
    """
    history = _read_json_file(HISTORY_FILE, [])
    if not isinstance(history, list):
        return []
    if limit <= 0:
        return history
    return history[-limit:]


def make_history_record(winner: str | None, first_player: str, moves: int):
    """
    建立一筆標準格式歷史紀錄
    """
    return {
        "time": datetime.now().isoformat(timespec="seconds"),
        "winner": winner if winner in ("X", "O") else "draw",
        "first_player": first_player,
        "moves": int(moves),
    }


if __name__ == "__main__":
    # 簡單自測（不影響被 import）
    gs = GameState(3)
    gs.set_move(0, 0, "X")
    gs.set_move(0, 1, "X")
    gs.set_move(0, 2, "X")
    print("Winner (預期 X):", check_winner(gs.board))
    print("Winning cells:", get_winning_cells(gs.board))
    print("Is draw:", is_draw(gs.board))

    # 測試 stats/history
    s = update_stats("X")
    print("Stats updated:", s)
    append_history(make_history_record("X", "X", 3))
    print("Recent history:", load_history(5))
