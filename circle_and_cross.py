import tkinter as tk
import random
import time

from ttt_lib import (
    GameState, check_winner, is_draw, get_winning_cells,
    load_stats, update_stats,
    load_history, append_history, make_history_record
)

"""
circle_and_cross.py - Tkinter 主程式（C5 版本）

在 C4 的基礎上新增：
- 隨機先手（random）
- 時間顯示（time）
- 戰績統計顯示（讀寫 ttt_stats.json）
- 歷史紀錄視窗（讀寫 ttt_history.json）

保留：
- 重新開始按鈕
- 遊戲結束禁用棋盤
- 勝利線標示（用 relief 樣式）
"""

BOARD_SIZE = 3

game_state: GameState | None = None
current_player = "X"
first_player = "X"
buttons: list[list[tk.Button]] = []

status_label: tk.Label
time_label: tk.Label
stats_label: tk.Label


def set_board_enabled(enabled: bool):
    state = tk.NORMAL if enabled else tk.DISABLED
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c].config(state=state)


def reset_button_styles():
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c].config(relief=tk.RAISED)


def mark_winning_cells(cells: list[tuple[int, int]]):
    for (r, c) in cells:
        buttons[r][c].config(relief=tk.SUNKEN)


def update_board_ui():
    if game_state is None:
        return
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c]["text"] = game_state.board[r][c]


def update_status_label():
    status_label["text"] = f"輪到玩家：{current_player}（先手：{first_player}）"


def count_moves_on_board() -> int:
    if game_state is None:
        return 0
    cnt = 0
    for row in game_state.board:
        for cell in row:
            if cell != "":
                cnt += 1
    return cnt


def refresh_stats_label():
    s = load_stats()
    stats_label["text"] = f"戰績：X勝 {s['X']}｜O勝 {s['O']}｜平手 {s['draw']}｜總局 {s['total']}"


def tick_time():
    now_str = time.strftime("%H:%M:%S")
    time_label["text"] = f"現在時間：{now_str}"
    time_label.after(1000, tick_time)


def start_new_game():
    global game_state, current_player, first_player

    game_state = GameState(BOARD_SIZE)

    # C5：隨機先手
    first_player = random.choice(["X", "O"])
    current_player = first_player

    reset_button_styles()
    update_board_ui()
    set_board_enabled(True)
    update_status_label()


def end_game_with_result(winner: str | None, winning_cells=None):
    """
    winner:
      - "X"/"O"：某一方獲勝
      - None：平手
    """
    # 1) UI 顯示
    if winner in ("X", "O"):
        status_label["text"] = f"玩家 {winner} 獲勝！（先手：{first_player}）"
    else:
        status_label["text"] = f"平手！（先手：{first_player}）"

    # 2) 標示勝利線
    if winning_cells:
        mark_winning_cells(winning_cells)

    # 3) 停止下棋
    if game_state is not None:
        game_state.set_game_over()
    set_board_enabled(False)

    # 4) 更新統計（存檔）
    update_stats(winner if winner in ("X", "O") else None)
    refresh_stats_label()

    # 5) 寫入歷史（存檔）
    moves = count_moves_on_board()
    record = make_history_record(winner if winner in ("X", "O") else None, first_player, moves)
    append_history(record)


def on_cell_click(row, col):
    global current_player

    if game_state is None:
        return
    if game_state.is_game_over():
        return
    if not game_state.is_cell_empty(row, col):
        return

    game_state.set_move(row, col, current_player)
    update_board_ui()

    winner = check_winner(game_state.board)
    if winner is not None:
        cells = get_winning_cells(game_state.board)
        end_game_with_result(winner, winning_cells=cells)
        return

    if is_draw(game_state.board):
        end_game_with_result(None)
        return

    current_player = "O" if current_player == "X" else "X"
    update_status_label()


def create_board(root):
    global buttons
    buttons = []
    for r in range(BOARD_SIZE):
        row_btns = []
        for c in range(BOARD_SIZE):
            btn = tk.Button(
                root,
                text="",
                width=5,
                height=2,
                font=("Helvetica", 20),
                command=lambda rr=r, cc=c: on_cell_click(rr, cc)
            )
            btn.grid(row=r + 1, column=c, padx=5, pady=5)
            row_btns.append(btn)
        buttons.append(row_btns)


def show_history_window():
    """
    顯示最近 20 筆歷史紀錄（新的在下面）
    """
    win = tk.Toplevel()
    win.title("對戰歷史（最近 20 筆）")

    history = load_history(limit=20)

    header = tk.Label(win, text="時間｜獲勝結果｜先手｜步數", font=("Helvetica", 12, "bold"))
    header.pack(padx=10, pady=(10, 5), anchor="w")

    text = tk.Text(win, width=50, height=15)
    text.pack(padx=10, pady=5)

    if not history:
        text.insert("end", "（目前沒有歷史紀錄）\n")
    else:
        for rec in history:
            t = rec.get("time", "")
            w = rec.get("winner", "")
            fp = rec.get("first_player", "")
            mv = rec.get("moves", "")
            line = f"{t}｜{w}｜{fp}｜{mv}\n"
            text.insert("end", line)

    text.config(state=tk.DISABLED)

    close_btn = tk.Button(win, text="關閉", command=win.destroy)
    close_btn.pack(pady=(0, 10))


def main():
    global status_label, time_label, stats_label

    root = tk.Tk()
    root.title("圈圈叉叉 - C5 統計+歷史+時間版")

    title_label = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 24))
    title_label.grid(row=0, column=0, columnspan=BOARD_SIZE, pady=10)

    create_board(root)

    status_label = tk.Label(root, text="", font=("Helvetica", 14))
    status_label.grid(row=BOARD_SIZE + 1, column=0, columnspan=BOARD_SIZE, pady=6)

    time_label = tk.Label(root, text="", font=("Helvetica", 12))
    time_label.grid(row=BOARD_SIZE + 2, column=0, columnspan=BOARD_SIZE, pady=2)

    stats_label = tk.Label(root, text="", font=("Helvetica", 12))
    stats_label.grid(row=BOARD_SIZE + 3, column=0, columnspan=BOARD_SIZE, pady=2)

    # 按鈕列
    btn_frame = tk.Frame(root)
    btn_frame.grid(row=BOARD_SIZE + 4, column=0, columnspan=BOARD_SIZE, pady=10)

    reset_btn = tk.Button(btn_frame, text="重新開始", font=("Helvetica", 12), command=start_new_game)
    reset_btn.pack(side="left", padx=6)

    history_btn = tk.Button(btn_frame, text="查看歷史", font=("Helvetica", 12), command=show_history_window)
    history_btn.pack(side="left", padx=6)

    # 初始化顯示
    refresh_stats_label()
    start_new_game()
    tick_time()

    root.mainloop()


if __name__ == "__main__":
    main()
