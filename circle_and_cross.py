import tkinter as tk
from ttt_lib import GameState, check_winner, is_draw   

"""
circle_and_cross.py - Tkinter 主程式（C1版本）

此版本目的：
- 建立視窗、標題
- 尚未加入棋盤按鈕與遊戲流程
- 先與 ttt_lib 做基本連結（import）
"""

def main():
    root = tk.Tk()
    root.title("圈圈叉叉 ")

    # 標題
    title_label = tk.Label(root, text="Tic Tac Toe", font=("Helvetica", 24))
    title_label.pack(pady=20)

    # 棋盤按鈕（3x3）
    placeholder = tk.Label(root, text="（棋盤介面）", font=("Helvetica", 12))
    placeholder.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
