import random
import tkinter as tk
from tkinter import messagebox, ttk
import time
import json
import os

class GuessTheNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Number Pro")
        self.master.geometry("500x400")
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

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Guess the Number Pro", font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.name_label = ttk.Label(self.main_frame, text="Player Name:")
        self.name_label.grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = ttk.Entry(self.main_frame)
        self.name_entry.grid(row=1, column=1, sticky="ew", pady=5)

        self.difficulty_label = ttk.Label(self.main_frame, text="Select Difficulty:")
        self.difficulty_label.grid(row=2, column=0, sticky="w", pady=5)
        self.difficulty_var = tk.StringVar()
        self.difficulty_combo = ttk.Combobox(self.main_frame, textvariable=self.difficulty_var, 
                                             values=["Easy", "Medium", "Hard"], state="readonly")
        self.difficulty_combo.grid(row=2, column=1, sticky="ew", pady=5)
        self.difficulty_combo.set("Medium")

        self.start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.info_label = ttk.Label(self.main_frame, text="")
        self.info_label.grid(row=4, column=0, columnspan=2, pady=5)

        self.guess_frame = ttk.Frame(self.main_frame)
        self.guess_frame.grid(row=5, column=0, columnspan=2, pady=5)

        self.guess_entry = ttk.Entry(self.guess_frame, width=10)
        self.guess_entry.pack(side=tk.LEFT, padx=5)

        self.submit_button = ttk.Button(self.guess_frame, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack(side=tk.LEFT)

        self.result_label = ttk.Label(self.main_frame, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.attempts_label = ttk.Label(self.main_frame, text="")
        self.attempts_label.grid(row=7, column=0, columnspan=2, pady=5)

        self.score_label = ttk.Label(self.main_frame, text="Score: 0")
        self.score_label.grid(row=8, column=0, columnspan=2, pady=5)

        self.leaderboard_button = ttk.Button(self.main_frame, text="Show Leaderboard", command=self.show_leaderboard)
        self.leaderboard_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.disable_game_widgets()

    def disable_game_widgets(self):
        self.guess_entry.config(state="disabled")
        self.submit_button.config(state="disabled")

    def enable_game_widgets(self):
        self.guess_entry.config(state="normal")
        self.submit_button.config(state="normal")

    def start_game(self):
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showerror("Invalid Name", "Please enter a player name.")
            return

        difficulty = self.difficulty_var.get().lower()
        self.min_num, self.max_num = self.get_range(difficulty)
        self.number = random.randint(self.min_num, self.max_num)
        self.attempts = 0
        self.max_attempts = 10 if difficulty == "easy" else (7 if difficulty == "medium" else 5)
        self.start_time = time.time()
        self.score = 0

        self.info_label.config(text=f"I'm thinking of a number between {self.min_num} and {self.max_num}.")
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        self.result_label.config(text="")
        self.score_label.config(text="Score: 0")

        self.enable_game_widgets()
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def get_range(self, difficulty):
        if difficulty == "easy":
            return 1, 50
        elif difficulty == "medium":
            return 1, 100
        else:
            return 1, 200

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

        if guess < self.number:
            self.result_label.config(text="Too low!")
        elif guess > self.number:
            self.result_label.config(text="Too high!")
        else:
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)
            self.calculate_score(time_taken)
            messagebox.showinfo("Congratulations!", 
                                f"Correct! You guessed it in {self.attempts} attempts and {time_taken} seconds.\nYour score: {self.score}")
            self.update_leaderboard()
            self.disable_game_widgets()
            return

        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")

        if self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", f"You've run out of attempts. The number was {self.number}.")
            self.disable_game_widgets()

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def calculate_score(self, time_taken):
        difficulty_multiplier = 1 if self.difficulty_var.get().lower() == "easy" else (2 if self.difficulty_var.get().lower() == "medium" else 3)
        time_factor = max(0, 100 - int(time_taken))
        attempts_factor = max(0, self.max_attempts - self.attempts)
        self.score = (time_factor + attempts_factor * 10) * difficulty_multiplier

    def update_leaderboard(self):
        self.leaderboard.append({
            "name": self.player_name,
            "score": self.score,
            "difficulty": self.difficulty_var.get()
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
        leaderboard_window.geometry("300x200")

        leaderboard_frame = ttk.Frame(leaderboard_window, padding="10")
        leaderboard_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(leaderboard_frame, text="Top 10 Scores", font=("Arial", 14, "bold")).pack(pady=5)

        for idx, entry in enumerate(self.leaderboard, start=1):
            ttk.Label(leaderboard_frame, text=f"{idx}. {entry['name']} - {entry['score']} ({entry['difficulty']})").pack()

def main():
    root = tk.Tk()
    GuessTheNumberGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()