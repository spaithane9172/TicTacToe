
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
from PIL import Image, ImageTk
import random

# -------------------- Configuration --------------------

BASE_DIR = Path(__file__).resolve().parent
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750

window = tk.Tk()
window.title("Tic Tac Toe")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
window.minsize(600, 550)
window.configure(bg="#10152d")

# -------------------- Background --------------------

background_image = None
background_label = tk.Label(window, bg="#10152d")
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def resize_background(event=None):
    global background_image

    if event and event.widget != window:
        return

    try:
        image_path = BASE_DIR / "img/Simpback.png"

        if not image_path.exists():
            image_path = BASE_DIR / "img/1.png"

        if image_path.exists():
            original = Image.open(image_path).convert("RGB")
            width = max(window.winfo_width(), 600)
            height = max(window.winfo_height(), 550)

            resized = original.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(resized)
            background_label.configure(image=background_image)
            background_label.lower()

    except Exception as error:
        print("Background loading error:", error)

window.bind("<Configure>", resize_background)

# -------------------- Game State --------------------

player1_name = ""
player2_name = ""
game_mode = "computer"

board = [""] * 9
buttons = []
current_player = "X"
game_over = False
screen_widgets = []

WINNING_COMBINATIONS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6)
]

# -------------------- UI Helpers --------------------

def clear_screen():
    global screen_widgets

    for widget in screen_widgets:
        try:
            widget.destroy()
        except tk.TclError:
            pass

    screen_widgets = []
    buttons.clear()

def add_widget(widget):
    screen_widgets.append(widget)
    return widget

def create_panel():
    panel = add_widget(
        tk.Frame(
            window,
            bg="#10152d",
            padx=25,
            pady=25,
            highlightbackground="#8b5cf6",
            highlightthickness=2
        )
    )
    panel.place(relx=0.5, rely=0.5, anchor="center")
    return panel

def create_title(parent, text, size=28):
    return tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold"),
        bg="#10152d",
        fg="white"
    )

def create_button(parent, text, command, color="#7c3aed"):
    return tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 13, "bold"),
        bg=color,
        fg="white",
        activebackground="#a78bfa",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=12
    )

# -------------------- Main Menu --------------------

def main_menu():
    clear_screen()

    panel = create_panel()

    create_title(panel, "TIC TAC TOE", 32).pack(pady=(5, 8))

    tk.Label(
        panel,
        text="Choose your game mode",
        font=("Arial", 13),
        bg="#10152d",
        fg="#d1d5db"
    ).pack(pady=(0, 25))

    create_button(
        panel,
        "PLAYER VS PLAYER",
        lambda: name_screen("player")
    ).pack(fill="x", pady=8)

    create_button(
        panel,
        "PLAYER VS COMPUTER",
        lambda: name_screen("computer"),
        color="#0f766e"
    ).pack(fill="x", pady=8)

    tk.Label(
        panel,
        text="First player: X     Second player: O",
        font=("Arial", 10),
        bg="#10152d",
        fg="#d1d5db"
    ).pack(pady=(20, 0))

# -------------------- Player Names --------------------

def name_screen(mode):
    global game_mode

    game_mode = mode
    clear_screen()

    panel = create_panel()

    create_title(panel, "PLAYER DETAILS", 25).pack(pady=(0, 20))

    tk.Label(
        panel,
        text="Enter your name",
        bg="#10152d",
        fg="white",
        font=("Arial", 12)
    ).pack(anchor="w")

    name1_entry = tk.Entry(
        panel,
        font=("Arial", 14),
        width=25,
        justify="center"
    )
    name1_entry.pack(pady=(8, 18), ipady=6)
    name1_entry.focus_set()

    name2_entry = None

    if mode == "player":
        tk.Label(
            panel,
            text="Enter second player's name",
            bg="#10152d",
            fg="white",
            font=("Arial", 12)
        ).pack(anchor="w")

        name2_entry = tk.Entry(
            panel,
            font=("Arial", 14),
            width=25,
            justify="center"
        )
        name2_entry.pack(pady=(8, 18), ipady=6)

    def start_game():
        global player1_name, player2_name

        player1_name = name1_entry.get().strip()

        if not player1_name:
            messagebox.showwarning(
                "Missing name",
                "Please enter the first player's name."
            )
            return

        if mode == "player":
            player2_name = name2_entry.get().strip()

            if not player2_name:
                messagebox.showwarning(
                    "Missing name",
                    "Please enter the second player's name."
                )
                return

        else:
            player2_name = "Computer"

        start_new_game()

    create_button(
        panel,
        "START GAME",
        start_game,
        color="#0f766e"
    ).pack(fill="x", pady=(5, 10))

    create_button(
        panel,
        "BACK TO MENU",
        main_menu,
        color="#374151"
    ).pack(fill="x")

# -------------------- Start / Reset Game --------------------

def start_new_game():
    global board, current_player, game_over

    board = [""] * 9
    current_player = "X"
    game_over = False

    show_board()

def reset_game():
    start_new_game()

# -------------------- Game Board --------------------

def show_board():
    clear_screen()

    panel = create_panel()

    title = f"{player1_name}  VS  {player2_name}"
    create_title(panel, title, 20).pack(pady=(0, 8))

    status_label = add_widget(
        tk.Label(
            panel,
            text="",
            font=("Arial", 13, "bold"),
            bg="#10152d",
            fg="#facc15"
        )
    )
    status_label.pack(pady=(0, 15))

    board_frame = tk.Frame(panel, bg="#10152d")
    board_frame.pack()

    for index in range(9):
        button = tk.Button(
            board_frame,
            text="",
            font=("Arial", 30, "bold"),
            width=4,
            height=2,
            bg="#20294a",
            fg="white",
            activebackground="#374151",
            activeforeground="white",
            disabledforeground="white",
            relief="flat",
            cursor="hand2",
            command=lambda i=index: make_move(i)
        )

        button.grid(
            row=index // 3,
            column=index % 3,
            padx=4,
            pady=4,
            sticky="nsew"
        )

        buttons.append(button)

    for i in range(3):
        board_frame.grid_columnconfigure(i, weight=1)
        board_frame.grid_rowconfigure(i, weight=1)

    create_button(
        panel,
        "RESTART GAME",
        reset_game,
        color="#0f766e"
    ).pack(fill="x", pady=(18, 7))

    create_button(
        panel,
        "BACK TO MENU",
        main_menu,
        color="#374151"
    ).pack(fill="x")

    update_status(status_label)

    # Keep the status label available to the move handlers.
    window.status_label = status_label

def update_status(label=None):
    if label is None:
        label = getattr(window, "status_label", None)

    if label is None:
        return

    if current_player == "X":
        name = player1_name
    else:
        name = player2_name

    label.config(text=f"{name}'s turn ({current_player})")

# -------------------- Game Logic --------------------

def get_winner():
    for a, b, c in WINNING_COMBINATIONS:
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], (a, b, c)

    return None, None

def finish_game(winner, winning_cells=None):
    global game_over

    game_over = True

    if winning_cells:
        for index in winning_cells:
            buttons[index].config(bg="#15803d")

    for button in buttons:
        button.config(state="disabled")

    if winner == "X":
        message = f"{player1_name} wins!"
    elif winner == "O":
        message = f"{player2_name} wins!"
    else:
        message = "It's a draw!"

    window.status_label.config(text=message)

def make_move(index):
    global current_player

    if game_over or board[index]:
        return

    # Prevent the player from moving during the computer's turn.
    if game_mode == "computer" and current_player == "O":
        return

    apply_move(index)

    if game_over:
        return

    if game_mode == "computer" and current_player == "O":
        window.after(400, computer_move)

def apply_move(index):
    global current_player

    if game_over or board[index]:
        return

    board[index] = current_player

    buttons[index].config(
        text=current_player,
        fg="#c084fc" if current_player == "X" else "#5eead4",
        disabledforeground="#c084fc" if current_player == "X" else "#5eead4",
        state="disabled"
    )

    winner, winning_cells = get_winner()

    if winner:
        finish_game(winner, winning_cells)
        return

    if all(board):
        finish_game(None)
        return

    current_player = "O" if current_player == "X" else "X"
    update_status()

def computer_move():
    if game_over or current_player != "O":
        return

    available = [
        index for index, value in enumerate(board)
        if not value
    ]

    if available:
        apply_move(random.choice(available))

# -------------------- Launch --------------------

main_menu()
window.mainloop()
