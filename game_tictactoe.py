
import customtkinter as ctk
from tkinter import messagebox
from config import get_db

PRIMARY = "#ff8fb7"
PRIMARY_HOVER = "#ff6b98"
BG = "#ffe6ef"
TEXT = "#5a3e47"


def save_score(user_id, result):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO games_scores (user_id, game_name, score) VALUES (%s, %s, %s)",
                (user_id, "tictactoe", result))
    conn.commit()
    cur.close()
    conn.close()


def tictactoe_gui(p1, p2):
    app = ctk.CTk()
    app.title("Tic Tac Toe 💞")
    app.geometry("360x430")
    app.configure(fg_color=BG)

    current_player = [p1]
    marks = {p1: "💗", p2: "✨"}  # << Heart Style
    board = [[" "]*3 for _ in range(3)]
    buttons = [[None]*3 for _ in range(3)]

    def check_win(mark):
        # rows
        for row in board:
            if row == [mark, mark, mark]:
                return True
        # columns
        for col in range(3):
            if board[0][col] == mark and board[1][col] == mark and board[2][col] == mark:
                return True
        # diagonals
        if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark:
            return True
        if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark:
            return True
        return False

    def check_draw():
        return all(board[r][c] != " " for r in range(3) for c in range(3))

    def make_move(r, c):
        if board[r][c] != " ":
            return

        mark = marks[current_player[0]]
        board[r][c] = mark
        buttons[r][c].configure(text=mark, font=("Arial", 38))

        if check_win(mark):
            save_score(current_player[0], 1)
            messagebox.showinfo("Winner 💗", f"Player {current_player[0]} wins!")
            app.destroy()
            return

        if check_draw():
            save_score(p1, 0.5)
            save_score(p2, 0.5)
            messagebox.showinfo("Draw 🤝", "It's a tie!")
            app.destroy()
            return

        current_player[0] = p2 if current_player[0] == p1 else p1

    title = ctk.CTkLabel(app, text="TIC TAC TOE 💞", font=("Arial", 22, "bold"), text_color=TEXT)
    title.pack(pady=15)

    board_frame = ctk.CTkFrame(app, fg_color=BG)
    board_frame.pack(pady=15)

    for r in range(3):
        for c in range(3):
            btn = ctk.CTkButton(
                board_frame,
                text="",
                width=85,
                height=85,
                corner_radius=50,  # round bubble 🫧
                fg_color="white",
                text_color=TEXT,
                hover_color=PRIMARY_HOVER,
                command=lambda r=r, c=c: make_move(r, c)
            )
            btn.grid(row=r, column=c, padx=5, pady=5)
            buttons[r][c] = btn

    app.mainloop()
