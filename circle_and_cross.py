import tkinter as tk
from ttt_lib import GameState, check_winner, is_draw   

"""
circle_and_cross.py - Tkinter 主程式（C2 版本）

此版本目的：
- 繼 C1 之後，新增 3x3 棋盤按鈕
- 目前按鈕的行為僅是：按下去顯示 "X"
- 尚未與 GameState（ttt_lib）做真正連動
"""

BOARD_SIZE = 3
buttons = []  # 之後用來存 3x3 按鈕


def on_cell_click(row, col):
    """
    C2 版本的暫時行為：
    - 如果該格子目前是空字串，就把按鈕文字設為 "X"
    - 尚未使用 GameState 或檢查勝負
    """
    btn = buttons[row][col]
    if btn["text"] == "":
        btn["text"] = "X"


def create_board(root):
    """建立 3x3 棋盤按鈕並排列在視窗中"""
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
            # 棋盤放在視窗上較上方的位置
            btn.grid(row=r + 1, column=c, padx=5, pady=5)
            row_btns.append(btn)
        buttons.append(row_btns)


def main():
    root = tk.Tk()
    root.title("圈圈叉叉 - C2 棋盤 UI")

    # 標題列（放在第 0 列）
    title_label = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 24))
    title_label.grid(row=0, column=0, columnspan=BOARD_SIZE, pady=10)

    # 建立棋盤按鈕（從 row=1 開始排）
    create_board(root)

    root.mainloop()


if __name__ == "__main__":
    main()
