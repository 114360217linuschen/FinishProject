import tkinter as tk
from ttt_lib import GameState, check_winner, is_draw, get_winning_cells

"""
circle_and_cross.py - Tkinter 主程式（C4 版本）

相較 C3：
- 新增「重新開始」按鈕
- 遊戲結束時禁用所有格子（避免繼續點）
- 若有人獲勝，標示勝利連線（用 relief/disabled 方式呈現）
"""

BOARD_SIZE = 3

game_state: GameState | None = None
current_player = "X"
buttons: list[list[tk.Button]] = []
status_label: tk.Label


def set_board_enabled(enabled: bool):
    """啟用/禁用棋盤按鈕"""
    state = tk.NORMAL if enabled else tk.DISABLED
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c].config(state=state)


def reset_button_styles():
    """清除所有按鈕的樣式標示（例如 winner 線）"""
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c].config(relief=tk.RAISED)


def mark_winning_cells(cells: list[tuple[int, int]]):
    """
    用按鈕的 relief 做簡單標示（不依賴顏色，跨平台較穩）
    """
    for (r, c) in cells:
        buttons[r][c].config(relief=tk.SUNKEN)


def update_board_ui():
    """依照 game_state.board 更新每個按鈕的文字"""
    if game_state is None:
        return
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c]["text"] = game_state.board[r][c]


def update_status_label():
    status_label["text"] = f"輪到玩家：{current_player}"


def start_new_game():
    """重開新局：重建 GameState、清空棋盤、重設玩家、恢復按鈕可點"""
    global game_state, current_player
    game_state = GameState(BOARD_SIZE)
    current_player = "X"

    reset_button_styles()
    update_board_ui()
    set_board_enabled(True)
    update_status_label()


def end_game_with_message(message: str, winning_cells=None):
    """統一處理遊戲結束：更新文字、禁用棋盤、標示勝利線"""
    status_label["text"] = message
    if winning_cells:
        mark_winning_cells(winning_cells)
    if game_state is not None:
        game_state.set_game_over()
    set_board_enabled(False)


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
        end_game_with_message(f"玩家 {winner} 獲勝！", winning_cells=cells)
        return

    if is_draw(game_state.board):
        end_game_with_message("平手！")
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


def main():
    global status_label

    root = tk.Tk()
    root.title("圈圈叉叉 - C4 重開+勝利線版本")

    title_label = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 24))
    title_label.grid(row=0, column=0, columnspan=BOARD_SIZE, pady=10)

    create_board(root)

    status_label = tk.Label(root, text="", font=("Helvetica", 14))
    status_label.grid(row=BOARD_SIZE + 1, column=0, columnspan=BOARD_SIZE, pady=8)

    # 重新開始按鈕
    reset_btn = tk.Button(root, text="重新開始", font=("Helvetica", 12), command=start_new_game)
    reset_btn.grid(row=BOARD_SIZE + 2, column=0, columnspan=BOARD_SIZE, pady=8)

    start_new_game()
    root.mainloop()


if __name__ == "__main__":
    main()
