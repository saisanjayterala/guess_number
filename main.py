import random
import tkinter as tk
from tkinter import messagebox, ttk
import time

class GuessTheNumberGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Guess the Number")
        self.master.geometry("400x300")
        self.master.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.number = None
        self.attempts = 0
        self.max_attempts = 0
        self.min_num = 0
        self.max_num = 0
        self.start_time = None

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.master, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Guess the Number", font=("Arial", 18, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.difficulty_label = ttk.Label(self.main_frame, text="Select Difficulty:")
        self.difficulty_label.grid(row=1, column=0, sticky="w", pady=5)

        self.difficulty_var = tk.StringVar()
        self.difficulty_combo = ttk.Combobox(self.main_frame, textvariable=self.difficulty_var, 
                                             values=["Easy", "Medium", "Hard"], state="readonly")
        self.difficulty_combo.grid(row=1, column=1, sticky="ew", pady=5)
        self.difficulty_combo.set("Medium")

        self.start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.info_label = ttk.Label(self.main_frame, text="")
        self.info_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.guess_frame = ttk.Frame(self.main_frame)
        self.guess_frame.grid(row=4, column=0, columnspan=2, pady=5)

        self.guess_entry = ttk.Entry(self.guess_frame, width=10)
        self.guess_entry.pack(side=tk.LEFT, padx=5)

        self.submit_button = ttk.Button(self.guess_frame, text="Submit Guess", command=self.check_guess)
        self.submit_button.pack(side=tk.LEFT)

        self.result_label = ttk.Label(self.main_frame, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=5)

        self.attempts_label = ttk.Label(self.main_frame, text="")
        self.attempts_label.grid(row=6, column=0, columnspan=2, pady=5)

        self.disable_game_widgets()

    def disable_game_widgets(self):
        self.guess_entry.config(state="disabled")
        self.submit_button.config(state="disabled")

    def enable_game_widgets(self):
        self.guess_entry.config(state="normal")
        self.submit_button.config(state="normal")

    def start_game(self):
        difficulty = self.difficulty_var.get().lower()
        self.min_num, self.max_num = self.get_range(difficulty)
        self.number = random.randint(self.min_num, self.max_num)
        self.attempts = 0
        self.max_attempts = 10 if difficulty == "easy" else (7 if difficulty == "medium" else 5)
        self.start_time = time.time()

        self.info_label.config(text=f"I'm thinking of a number between {self.min_num} and {self.max_num}.")
        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")
        self.result_label.config(text="")

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
            messagebox.showinfo("Congratulations!", 
                                f"Correct! You guessed it in {self.attempts} attempts and {time_taken} seconds.")
            self.disable_game_widgets()
            return

        self.attempts_label.config(text=f"Attempts: {self.attempts}/{self.max_attempts}")

        if self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", f"You've run out of attempts. The number was {self.number}.")
            self.disable_game_widgets()

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

def main():
    root = tk.Tk()
    GuessTheNumberGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()