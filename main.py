import random
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import time
import json
import os
from PIL import Image, ImageTk
import pygame
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GuessTheNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Number Ultimate")
        self.master.geometry("700x600")
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
        self.game_history = []
        self.current_streak = 0
        self.best_streak = 0
        self.total_games_played = 0
        self.total_wins = 0
        self.sound_enabled = True
        self.theme = "light"

        self.load_images()
        self.load_sounds()
        self.create_widgets()
        self.create_menu()

    def load_images(self):
        self.logo = ImageTk.PhotoImage(Image.open("logo.png").resize((100, 100)))
        self.hint_icon = ImageTk.PhotoImage(Image.open("hint.png").resize((20, 20)))
        self.sound_on_icon = ImageTk.PhotoImage(Image.open("sound_on.png").resize((20, 20)))
        self.sound_off_icon = ImageTk.PhotoImage(Image.open("sound_off.png").resize((20, 20)))

    def load_sounds(self):
        pygame.mixer.init()
        self.correct_sound = pygame.mixer.Sound("correct.wav")
        self.wrong_sound = pygame.mixer.Sound("wrong.wav")
        self.hint_sound = pygame.mixer.Sound("hint.wav")

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
                                             values=["Easy", "Medium", "Hard", "Expert", "Custom"], state="readonly")
        self.difficulty_combo.grid(row=3, column=1, columnspan=2, sticky="ew", pady=5)
        self.difficulty_combo.set("Medium")
        self.difficulty_combo.bind("<<ComboboxSelected>>", self.on_difficulty_change)

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

        self.sound_button = ttk.Button(self.guess_frame, image=self.sound_on_icon, command=self.toggle_sound)
        self.sound_button.pack(side=tk.LEFT, padx=5)

        self.result_label = ttk.Label(self.main_frame, text="")
        self.result_label.grid(row=7, column=0, columnspan=3, pady=5)

        self.attempts_label = ttk.Label(self.main_frame, text="")
        self.attempts_label.grid(row=8, column=0, columnspan=3, pady=5)

        self.score_label = ttk.Label(self.main_frame, text="Score: 0")
        self.score_label.grid(row=9, column=0, columnspan=3, pady=5)

        self.streak_label = ttk.Label(self.main_frame, text="Current Streak: 0 | Best Streak: 0")
        self.streak_label.grid(row=10, column=0, columnspan=3, pady=5)

        self.progress_bar = ttk.Progressbar(self.main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=11, column=0, columnspan=3, pady=10)

        self.stats_button = ttk.Button(self.main_frame, text="Show Statistics", command=self.show_statistics)
        self.stats_button.grid(row=12, column=0, columnspan=3, pady=5)

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

        options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=options_menu)
        options_menu.add_command(label="Toggle Sound", command=self.toggle_sound)
        options_menu.add_command(label="Toggle Theme", command=self.toggle_theme)

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

        self.total_games_played += 1

    def get_range(self, difficulty):
        if difficulty == "easy":
            return 1, 50
        elif difficulty == "medium":
            return 1, 100
        elif difficulty == "hard":
            return 1, 200
        elif difficulty == "expert":
            return 1, 500
        else:  # Custom
            min_num = simpledialog.askinteger("Custom Range", "Enter the minimum number:", minvalue=1, maxvalue=9999)
            max_num = simpledialog.askinteger("Custom Range", "Enter the maximum number:", minvalue=min_num, maxvalue=10000)
            return min_num, max_num

    def get_max_attempts(self, difficulty):
        if difficulty == "easy":
            return 10
        elif difficulty == "medium":
            return 7
        elif difficulty == "hard":
            return 5
        elif difficulty == "expert":
            return 3
        else:  # Custom
            return simpledialog.askinteger("Custom Attempts", "Enter the maximum number of attempts:", minvalue=1, maxvalue=20)

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
            if self.sound_enabled:
                self.wrong_sound.play()
        elif guess > self.number:
            self.result_label.config(text="Too high!")
            if self.sound_enabled:
                self.wrong_sound.play()
        else:
            if self.sound_enabled:
                self.correct_sound.play()
            end_time = time.time()
            time_taken = round(end_time - self.start_time, 2)
            self.calculate_score(time_taken)
            messagebox.showinfo("Congratulations!", 
                                f"Correct! You guessed it in {self.attempts} attempts and {time_taken} seconds.\n"
                                f"Your score: {self.score}\nHints used: {self.hints_used}")
            self.update_leaderboard()
            self.update_game_history(True)
            self.update_streak(True)
            self.total_wins += 1
            self.disable_game_widgets()
            return

        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")

        if self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", f"You've run out of attempts. The number was {self.number}.")
            self.update_game_history(False)
            self.update_streak(False)
            self.disable_game_widgets()

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def give_hint(self):
        if self.number is None:
            return

        hint_type = random.choice(["parity", "multiple", "range", "digit_sum", "prime"])

        if hint_type == "parity":
            hint = "even" if self.number % 2 == 0 else "odd"
            message = f"The number is {hint}."
        elif hint_type == "multiple":
            factor = random.choice([2, 3, 5, 7])
            if self.number % factor == 0:
                message = f"The number is a multiple of {factor}."
            else:
                message = f"The number is not a multiple of {factor}."
        elif hint_type == "range":
            range_size = (self.max_num - self.min_num) // 4
            lower = self.number - random.randint(1, range_size)
            upper = self.number + random.randint(1, range_size)
            message = f"The number is between {max(self.min_num, lower)} and {min(self.max_num, upper)}."
        elif hint_type == "digit_sum":
            digit_sum = sum(int(d) for d in str(self.number))
            message = f"The sum of the digits in the number is {digit_sum}."
        else:  # prime
            is_prime = all(self.number % i != 0 for i in range(2, int(self.number ** 0.5) + 1))
            if is_prime:
                message = "The number is prime."
            else:
                message = "The number is not prime."

        messagebox.showinfo("Hint", message)
        self.hints_used += 1
        self.score -= 10
        self.score_label.config(text=f"Score: {self.score}")

        if self.sound_enabled:
            self.hint_sound.play()

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
        elif difficulty == "expert":
            return 4
        else:  # Custom
            return 2  # Default multiplier for custom difficulty

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
        leaderboard_window.geometry("500x400")

        leaderboard_frame = ttk.Frame(leaderboard_window, padding="10")
        leaderboard_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(leaderboard_frame, text="Top 10 Scores", font=("Arial", 14, "bold")).pack(pady=5)

        columns = ("Rank", "Name", "Score", "Difficulty", "Attempts", "Hints")
        tree = ttk.Treeview(leaderboard_frame, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=70, anchor="center")

        tree.column("Name", width=120)

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
        4. Use hints if you need help (costs 10 points per hint).
        5. Try to guess the number in as few attempts as possible.
        6. Your score is based on time, attempts, difficulty, and hints used.
        7. Maintain a streak by winning consecutive games.
        8. View your statistics to track your progress.
        """
        messagebox.showinfo("How to Play", help_text)

    def show_about(self):
        about_text = """
        Guess the Number Ultimate
        Version 3.0

        Created by Your Name
        Copyright © 2024

        Features:
        - Multiple difficulty levels
        - Custom game settings
        - Leaderboard
        - Statistics tracking
        - Sound effects
        - Themes
        """
        messagebox.showinfo("About", about_text)

    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        icon = self.sound_on_icon if self.sound_enabled else self.sound_off_icon
        self.sound_button.config(image=icon)

    def toggle_theme(self):
        if self.theme == "light":
            self.theme = "dark"
            self.style.theme_use('clam')
            self.style.configure(".", background="#2E2E2E", foreground="white")
            self.style.configure("TButton", background="#4A4A4A", foreground="white")
            self.style.configure("TEntry", fieldbackground="#4A4A4A", foreground="white")
            self.style.configure("TLabel", background="#2E2E2E", foreground="white")
        else:
            self.theme = "light"
            self.style.theme_use('clam')
            self.style.configure(".", background="white", foreground="black")
            self.style.configure("TButton", background="#E0E0E0", foreground="black")
            self.style.configure("TEntry", fieldbackground="white", foreground="black")
            self.style.configure("TLabel", background="white", foreground="black")

    def update_game_history(self, win):
        self.game_history.append({
            "difficulty": self.difficulty_var.get(),
            "win": win,
            "attempts": self.attempts,
            "hints": self.hints_used,
            "score": self.score
        })

    def update_streak(self, win):
        if win:
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0
        self.streak_label.config(text=f"Current Streak: {self.current_streak} | Best Streak: {self.best_streak}")

    def show_statistics(self):
        stats_window = tk.Toplevel(self.master)
        stats_window.title("Game Statistics")
        stats_window.geometry("600x500")

        stats_frame = ttk.Frame(stats_window, padding="10")
        stats_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(stats_frame, text="Game Statistics", font=("Arial", 14, "bold")).pack(pady=5)

        stats_text = f"""
        Total Games Played: {self.total_games_played}
        Total Wins: {self.total_wins}
        Win Rate: {self.total_wins / self.total_games_played * 100:.2f}%
        Current Streak: {self.current_streak}
        Best Streak: {self.best_streak}
        """

        ttk.Label(stats_frame, text=stats_text, justify=tk.LEFT).pack(pady=10)

        self.create_difficulty_distribution_chart(stats_frame)
        self.create_score_distribution_chart(stats_frame)

    def create_difficulty_distribution_chart(self, parent):
        difficulties = [game["difficulty"] for game in self.game_history]
        difficulty_counts = {diff: difficulties.count(diff) for diff in set(difficulties)}

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(difficulty_counts.keys(), difficulty_counts.values())
        ax.set_title("Games by Difficulty")
        ax.set_xlabel("Difficulty")
        ax.set_ylabel("Number of Games")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def create_score_distribution_chart(self, parent):
        scores = [game["score"] for game in self.game_history]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(scores, bins=10)
        ax.set_title("Score Distribution")
        ax.set_xlabel("Score")
        ax.set_ylabel("Frequency")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    def on_difficulty_change(self, event):
        if self.difficulty_var.get() == "Custom":
            self.custom_difficulty_dialog()

    def custom_difficulty_dialog(self):
        custom_window = tk.Toplevel(self.master)
        custom_window.title("Custom Difficulty")
        custom_window.geometry("300x200")

        ttk.Label(custom_window, text="Min Number:").pack(pady=5)
        min_entry = ttk.Entry(custom_window)
        min_entry.pack(pady=5)

        ttk.Label(custom_window, text="Max Number:").pack(pady=5)
        max_entry = ttk.Entry(custom_window)
        max_entry.pack(pady=5)

        ttk.Label(custom_window, text="Max Attempts:").pack(pady=5)
        attempts_entry = ttk.Entry(custom_window)
        attempts_entry.pack(pady=5)

        def save_custom():
            try:
                self.min_num = int(min_entry.get())
                self.max_num = int(max_entry.get())
                self.max_attempts = int(attempts_entry.get())
                custom_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers.")

        ttk.Button(custom_window, text="Save", command=save_custom).pack(pady=10)

def main():
    root = tk.Tk()
    GuessTheNumberGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()