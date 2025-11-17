import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk, ImageFilter

# Global variables
score = 0
question_count = 0
correct_first_try = 0
correct_second_try = 0
wrong_total = 0

difficulty = 1
num1 = 0
num2 = 0
operation = ""
attempt = 0


def displayMenu():
    clearScreen()
    title = tk.Label(root, text="SELECT DIFFICULTY", font=("Arial", 26, "bold"),
                     bg="white", fg="#1b5e20")
    title.pack(pady=30)

    tk.Button(root, text="1. EASY", width=18, font=("Arial", 18),
              command=lambda: start_quiz(1)).pack(pady=10)
    tk.Button(root, text="2. MODERATE", width=18, font=("Arial", 18),
              command=lambda: start_quiz(2)).pack(pady=10)
    tk.Button(root, text="3. ADVANCED", width=18, font=("Arial", 18),
              command=lambda: start_quiz(3)).pack(pady=10)


def randomInt(level):
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    return random.choice(["+", "-"])


def start_quiz(level):
    global difficulty, score, question_count, correct_first_try, correct_second_try, wrong_total
    difficulty = level
    score = 0
    question_count = 0
    correct_first_try = 0
    correct_second_try = 0
    wrong_total = 0
    displayProblem()


def displayProblem():
    global num1, num2, operation, answer_entry

    clearScreen()

    if question_count >= 10:
        displayResults()
        return

    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    operation = decideOperation()

    # Question counter label
    counter_label = tk.Label(root, text=f"Question {question_count+1} of 10",
                             font=("Arial", 22, "bold"), bg="white")
    counter_label.pack(pady=10)

    problem = f"{num1} {operation} {num2} = ?"

    label = tk.Label(root, text="Solve the Problem:", font=("Arial", 24, "bold"),
                     bg="white")
    label.pack(pady=10)

    problem_label = tk.Label(root, text=problem, font=("Arial", 40, "bold"),
                             bg="white")
    problem_label.pack(pady=20)

    answer_entry = tk.Entry(root, font=("Arial", 22), justify="center")
    answer_entry.pack(pady=10)

    submit_btn = tk.Button(root, text="Submit", font=("Arial", 20),
                           command=checkAnswer)
    submit_btn.pack(pady=10)


def checkAnswer():
    global score, question_count, attempt, correct_first_try, correct_second_try, wrong_total
    try:
        user_answer = int(answer_entry.get())
    except:
        messagebox.showerror("Error", "Please enter a valid number!")
        return

    correct = num1 + num2 if operation == "+" else num1 - num2

    if user_answer == correct:
        if attempt == 0:
            score += 10
            correct_first_try += 1
        else:
            score += 5
            correct_second_try += 1

        messagebox.showinfo("Correct", "Correct! Good job!")
        attempt = 0
        nextQuestion()
    else:
        if attempt == 0:
            attempt += 1
            messagebox.showwarning("Try Again", "Incorrect! Try once more.")
        else:
            messagebox.showerror("Wrong", f"Wrong again! Correct answer was {correct}")
            wrong_total += 1
            attempt = 0
            nextQuestion()


def nextQuestion():
    global question_count
    question_count += 1
    displayProblem()


def displayResults():
    clearScreen()

    if score >= 90: grade = "A+"
    elif score >= 80: grade = "A"
    elif score >= 70: grade = "B"
    elif score >= 60: grade = "C"
    else: grade = "D"

    result_text = (
        f"FINAL SCORE: {score}/100\nGRADE: {grade}\n\n"
        f"Correct (1st try): {correct_first_try}\n"
        f"Correct (2nd try): {correct_second_try}\n"
        f"Wrong: {wrong_total}\n"
    )

    result_label = tk.Label(root, text=result_text,
                            font=("Arial", 26, "bold"), bg="white")
    result_label.pack(pady=40)

    tk.Button(root, text="Play Again", font=("Arial", 22), command=displayMenu).pack(pady=10)
    tk.Button(root, text="Exit", font=("Arial", 22), command=root.destroy).pack(pady=10)


def clearScreen():
    for widget in root.winfo_children():
        widget.destroy()

    # redraw blurred background
    bg_label = tk.Label(root, image=blur_bg_img)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# MAIN WINDOW
root = tk.Tk()
root.title("Math Quiz")
root.geometry("800x600")
root.resizable(False, False)

# LOAD BACKGROUND IMAGE WITH BLUR EFFECT
bg = Image.open("exercise 1\math_bg.jpg")
bg = bg.resize((800, 600))
bg = bg.filter(ImageFilter.GaussianBlur(radius=6)) # blur effect
blur_bg_img = ImageTk.PhotoImage(bg)

# Display initial background
bg_label = tk.Label(root, image=blur_bg_img)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

displayMenu()
root.mainloop()