import tkinter as tk
from ttt_lib import GameState, check_winner, is_draw

"""
circle_and_cross.py - Tkinter 主程式（C3 版本）

此版本目的：
- 新增 GameState 整合：
  - 不再讓按鈕自己記文字，而是由 GameState.board 管理棋盤
  - 每一步都從 board 更新按鈕顯示
- 使用 check_winner() / is_draw() 更新狀態列
- 顯示「輪到玩家：X / O」
"""

BOARD_SIZE = 3

# 全域變數：之後在 main() / start_new_game() 裡初始化
game_state: GameState | None = None
current_player = "X"
buttons: list[list[tk.Button]] = []
status_label: tk.Label


def update_board_ui():
    """依照 game_state.board 更新每個按鈕的文字"""
    if game_state is None:
        return
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            buttons[r][c]["text"] = game_state.board[r][c]


def update_status_label():
    """顯示目前輪到哪位玩家"""
    if game_state is None:
        status_label["text"] = ""
    else:
        status_label["text"] = f"輪到玩家：{current_player}"


def start_new_game():
    """開始一局新遊戲：重建 GameState，清空棋盤，重設玩家"""
    global game_state, current_player
    game_state = GameState(BOARD_SIZE)
    current_player = "X"
    update_board_ui()
    update_status_label()


def on_cell_click(row, col):
    """
    玩家在 (row, col) 點擊：
    - 若遊戲已結束 -> 不動作
    - 若該格不空 -> 不動作
    - 否則：
        1. 呼叫 game_state.set_move()
        2. 更新 UI
        3. check_winner() / is_draw()
        4. 更新狀態列與 game_over
    """
    global current_player

    if game_state is None:
        return

    # 遊戲結束就不再響應
    if game_state.is_game_over():
        return

    # 不允許覆寫已有棋子
    if not game_state.is_cell_empty(row, col):
        return

    # 由 GameState 負責記錄棋盤
    game_state.set_move(row, col, current_player)
    update_board_ui()

    # 檢查勝負
    winner = check_winner(game_state.board)
    if winner is not None:
        status_label["text"] = f"玩家 {winner} 獲勝！"
        game_state.set_game_over()
        return

    # 檢查平手
    if is_draw(game_state.board):
        status_label["text"] = "平手！"
        game_state.set_game_over()
        return

    # 尚未結束 -> 換人
    current_player = "O" if current_player == "X" else "X"
    update_status_label()


def create_board(root):
    """
    建立 3x3 棋盤按鈕：
    - 使用 grid() 佈局
    - row 從 1 開始，讓 row=0 留給標題
    """
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
    root.title("圈圈叉叉 - C3 GameState 整合版")

    # 標題列（第 0 列）
    title_label = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 24))
    title_label.grid(row=0, column=0, columnspan=BOARD_SIZE, pady=10)

    # 棋盤按鈕（第 1~3 列）
    create_board(root)

    # 狀態列（顯示輪到誰 / 誰贏 / 平手）
    status_label = tk.Label(root, text="", font=("Helvetica", 14))
    status_label.grid(row=BOARD_SIZE + 1, column=0, columnspan=BOARD_SIZE, pady=10)

    # 初始化一局新遊戲
    start_new_game()

    root.mainloop()


if __name__ == "__main__":
    main()
