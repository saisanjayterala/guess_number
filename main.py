import random
import time
import sys

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def get_difficulty():
    while True:
        difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
        if difficulty in ['easy', 'medium', 'hard']:
            return difficulty
        slow_print("Invalid input. Please choose easy, medium, or hard.")

def get_range(difficulty):
    if difficulty == 'easy':
        return 1, 50
    elif difficulty == 'medium':
        return 1, 100
    else:
        return 1, 200

def play_game():
    difficulty = get_difficulty()
    min_num, max_num = get_range(difficulty)
    number = random.randint(min_num, max_num)
    attempts = 0
    max_attempts = 10 if difficulty == 'easy' else (7 if difficulty == 'medium' else 5)
    
    slow_print(f"I'm thinking of a number between {min_num} and {max_num}.")
    slow_print(f"You have {max_attempts} attempts to guess it.")
    
    start_time = time.time()
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"Attempt {attempts + 1}/{max_attempts}. Enter your guess: "))
        except ValueError:
            slow_print("Please enter a valid number.")
            continue
        
        if guess < min_num or guess > max_num:
            slow_print(f"Your guess should be between {min_num} and {max_num}.")
            continue
        
        attempts += 1
        
        if guess < number:
            slow_print("Too low!")
        elif guess > number:
            slow_print("Too high!")
        else:
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            slow_print(f"Correct! You guessed it in {attempts} attempts and {time_taken} seconds.")
            return
        
        if attempts < max_attempts:
            slow_print(f"You have {max_attempts - attempts} attempts left.")
    
    slow_print(f"Game over! The number was {number}.")

def main():
    while True:
        slow_print("Welcome to Guess the Number!")
        play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            slow_print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    main()