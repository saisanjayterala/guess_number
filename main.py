import random
import tkinter as tk
from tkinter import messagebox, ttk
import time
import json
import os
from PIL import Image, ImageTk

class GuessTheNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Number Ultimate")
        self.master.geometry("600x500")
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.number = None
        self.attempts = 0
        self.max_attempts = 0
        self.min_num = 0
        self.max_num = 0
        self.start_time = None
        self.score = 0
        self.player_name = ""
        self.leaderboard = self.load_leaderboard()
        self.hints_used = 0

        self.load_images()
        self.create_widgets()
        self.create_menu()

    def load_images(self):
        self.logo = ImageTk.PhotoImage(Image.open("logo.png").resize((100, 100)))
        self.hint_icon = ImageTk.PhotoImage(Image.open("hint.png").resize((20, 20)))

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.main_frame, image=self.logo).grid(row=0, column=0, columnspan=3, pady=10)

        self.title_label = ttk.Label(self.main_frame, text="Guess the Number Ultimate", font=("Arial", 18, "bold"))
        self.title_label.grid(row=1, column=0, columnspan=3, pady=10)

        self.name_label = ttk.Label(self.main_frame, text="Player Name:")
        self.name_label.grid(row=2, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(self.main_frame)
        self.name_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=5)

        self.difficulty_label = ttk.Label(self.main_frame, text="Select Difficulty:")
        self.difficulty_label.grid(row=3, column=0, sticky="w", pady=5)
        self.difficulty_var = tk.StringVar()
        self.difficulty_combo = ttk.Combobox(self.main_frame, textvariable=self.difficulty_var, 
                                             values=["Easy", "Medium", "Hard", "Expert"], state="readonly")
        self.difficulty_combo.grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)
        self.difficulty_combo.set("Medium")

        self.start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.info_label = ttk.Label(self.main_frame, text="")
        self.info_label.grid(row=5, column=0, columnspan=3, pady=5)

        self.guess_frame = ttk.Frame(self.main_frame)
        self.guess_frame.grid(row=6, column=0, columnspan=3, pady=5)

        self.guess_entry = ttk.Entry(self.guess_frame, width=10)
        self.guess_entry.pack(side=tk.LEFT, padx=5)

        self.submit_button = ttk.Button(self.guess_frame, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack(side=tk.LEFT)

        self.hint_button = ttk.Button(self.guess_frame, image=self.hint_icon, command=self.give_hint)
        self.hint_button.pack(side=tk.LEFT, padx=5)

        self.result_label = ttk.Label(self.main_frame, text="")
        self.result_label.grid(row=7, column=0, columnspan=3, pady=5)

        self.attempts_label = ttk.Label(self.main_frame, text="")
        self.attempts_label.grid(row=8, column=0, columnspan=3, pady=5)

        self.score_label = ttk.Label(self.main_frame, text="Score: 0")
        self.score_label.grid(row=9, column=0, columnspan=3, pady=5)

        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=10, column=0, columnspan=3, pady=10)

        self.disable_game_widgets()

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="New Game", command=self.start_game)
        game_menu.add_command(label="Show Leaderboard", command=self.show_leaderboard)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="How to Play", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

    def disable_game_widgets(self):
        self.guess_entry.config(state="disabled")
        self.submit_button.config(state="disabled")
        self.hint_button.config(state="disabled")

    def enable_game_widgets(self):
        self.guess_entry.config(state="normal")
        self.submit_button.config(state="normal")
        self.hint_button.config(state="normal")

    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Invalid Name", "Please enter a player name.")
            return

        difficulty = self.difficulty_var.get().lower()
        self.min_num, self.max_num = self.get_range(difficulty)
        self.number = random.randint(self.min_num, self.max_num)
        self.attempts = 0
        self.max_attempts = self.get_max_attempts(difficulty)
        self.start_time = time.time()
        self.score = 0
        self.hints_used = 0

        self.info_label.config(text=f"I'm thinking of a number between {self.min_num} and {self.max_num}.")
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        self.result_label.config(text="")
        self.score_label.config(text="Score: 0")
        self.progress_bar["value"] = 0

        self.enable_game_widgets()
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def get_range(self, difficulty):
        if difficulty == "easy":
            return 1, 50
        elif difficulty == "medium":
            return 1, 100
        elif difficulty == "hard":
            return 1, 200
        else:  # Expert
            return 1, 500

    def get_max_attempts(self, difficulty):
        if difficulty == "easy":
            return 10
        elif difficulty == "medium":
            return 7
        elif difficulty == "hard":
            return 5
        else:  # Expert
            return 3

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")
            return

        if guess < self.min_num or guess > self.max_num:
            messagebox.showerror("Out of Range", f"Your guess should be between {self.min_num} and {self.max_num}.")
            return

        self.attempts += 1
        self.progress_bar["value"] = (self.attempts / self.max_attempts) * 100

        if guess < self.number:
            self.result_label.config(text="Too low!")
        elif guess > self.number:
            self.result_label.config(text="Too high!")
        else:
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)
            self.calculate_score(time_taken)
            messagebox.showinfo("Congratulations!", 
                                f"Correct! You guessed it in {self.attempts} attempts and {time_taken} seconds.\n"
                                f"Your score: {self.score}\nHints used: {self.hints_used}")
            self.update_leaderboard()
            self.disable_game_widgets()
            return

        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")

        if self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", f"You've run out of attempts. The number was {self.number}.")
            self.disable_game_widgets()

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def give_hint(self):
        if self.number is None:
            return

        hint_type = random.choice(["parity", "multiple", "range"])

        if hint_type == "parity":
            hint = "even" if self.number % 2 == 0 else "odd"
            message = f"The number is {hint}."
        elif hint_type == "multiple":
            factor = random.choice([2, 3, 5])
            if self.number % factor == 0:
                message = f"The number is a multiple of {factor}."
            else:
                message = f"The number is not a multiple of {factor}."
        else:
            range_size = (self.max_num - self.min_num) // 4
            lower = self.number - random.randint(1, range_size)
            upper = self.number + random.randint(1, range_size)
            message = f"The number is between {max(self.min_num, lower)} and {min(self.max_num, upper)}."

        messagebox.showinfo("Hint", message)
        self.hints_used += 1
        self.score -= 10
        self.score_label.config(text=f"Score: {self.score}")

    def calculate_score(self, time_taken):
        difficulty_multiplier = self.get_difficulty_multiplier()
        time_factor = max(0, 100 - int(time_taken))
        attempts_factor = max(0, self.max_attempts - self.attempts)
        self.score = (time_factor + attempts_factor * 10) * difficulty_multiplier - (self.hints_used * 5)

    def get_difficulty_multiplier(self):
        difficulty = self.difficulty_var.get().lower()
        if difficulty == "easy":
            return 1
        elif difficulty == "medium":
            return 2
        elif difficulty == "hard":
            return 3
        else:  # Expert
            return 4

    def update_leaderboard(self):
        self.leaderboard.append({
            "name": self.player_name,
            "score": self.score,
            "difficulty": self.difficulty_var.get(),
            "attempts": self.attempts,
            "hints": self.hints_used
        })
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.leaderboard = self.leaderboard[:10]  # Keep only top 10 scores
        self.save_leaderboard()

    def load_leaderboard(self):
        if os.path.exists("leaderboard.json"):
            with open("leaderboard.json", "r") as f:
                return json.load(f)
        return []

    def save_leaderboard(self):
        with open("leaderboard.json", "w") as f:
            json.dump(self.leaderboard, f)

    def show_leaderboard(self):
        leaderboard_window = tk.Toplevel(self.master)
        leaderboard_window.title("Leaderboard")
        leaderboard_window.geometry("400x300")

        leaderboard_frame = ttk.Frame(leaderboard_window, padding="10")
        leaderboard_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(leaderboard_frame, text="Top 10 Scores", font=("Arial", 14, "bold")).pack(pady=5)

        columns = ("Rank", "Name", "Score", "Difficulty", "Attempts", "Hints")
        tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=60, anchor="center")

        tree.column("Name", width=100)

        for idx, entry in enumerate(self.leaderboard, start=1):
            tree.insert("", "end", values=(idx, entry['name'], entry['score'], entry['difficulty'], 
                                           entry['attempts'], entry['hints']))

        tree.pack(fill=tk.BOTH, expand=True)

    def show_help(self):
        help_text = """
        How to Play:
        1. Enter your name and select a difficulty level.
        2. Click 'Start Game' to begin.
        3. Guess the number within the given range.
        4. Use hints if you need help (costs 5 points per hint).
        5. Try to guess the number in as few attempts as possible.
        6. Your score is based on time, attempts, difficulty, and hints used.
        """
        messagebox.showinfo("How to Play", help_text)

    def show_about(self):
        about_text = """
        Guess the Number Ultimate
        Version 2.0

        Created by Your Name
        Copyright © 2024
        """
        messagebox.showinfo("About", about_text)

def main():
    root = tk.Tk()
    GuessTheNumberGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()