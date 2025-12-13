# Student Manager App

import tkinter as tk
from tkinter import messagebox, simpledialog

FILE_PATH = "Assessment 1 - Skills Portfolio\A1 - Resources\studentMarks.txt"
TOTAL_MARKS = 160   # 3 coursework (20 each) + exam (100)

# ---------- FILE HANDLING ----------

# READ STUDENT DATA FROM FILE
def read_file():
    students = []
    try:
        with open(FILE_PATH, "r") as file:
            lines = file.readlines()

        total_students = int(lines[0].strip())

        for line in lines[1:1 + total_students]:
            parts = line.strip().split(',')
            students.append({
                "number": parts[0],
                "name": parts[1],
                "cw1": int(parts[2]),
                "cw2": int(parts[3]),
                "cw3": int(parts[4]),
                "exam": int(parts[5])
            })
    except:
        messagebox.showerror("Error", "Could not read studentMarks.txt")

    return students


# WRITE UPDATED DATA BACK TO FILE
def write_file(students):
    with open(FILE_PATH, "w") as file:
        file.write(str(len(students)) + "\n")
        for s in students:
            file.write(f"{s['number']},{s['name']},{s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n")


# ---------- CALCULATIONS ----------

# CALCULATE TOTAL MARKS
def get_total(s):
    return s['cw1'] + s['cw2'] + s['cw3'] + s['exam']


# CALCULATE OVERALL PERCENTAGE
def get_percentage(s):
    return (get_total(s) / TOTAL_MARKS) * 100


# ASSIGN GRADE
def get_grade(p):
    if p >= 70:
        return "A"
    elif p >= 60:
        return "B"
    elif p >= 50:
        return "C"
    elif p >= 40:
        return "D"
    else:
        return "F"


# ---------- GUI APPLICATION ----------

class StudentManager:
    def __init__(self, root):
        # INITIALIZE WINDOW
        self.root = root
        self.root.title("Student Manager")
        self.root.geometry("850x500")

        # LOAD STUDENT DATA
        self.students = read_file()

        # OUTPUT AREA
        self.output = tk.Text(root)
        self.output.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # MENU BUTTONS
        menu = tk.Frame(root)
        menu.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # ---------- MENU OPTIONS ----------
        tk.Button(menu, text="View All Students", width=20, command=self.view_all).pack(pady=2)
        tk.Button(menu, text="View Individual Student", width=20, command=self.view_one).pack(pady=2)
        tk.Button(menu, text="Highest Mark", width=20, command=self.highest).pack(pady=2)
        tk.Button(menu, text="Lowest Mark", width=20, command=self.lowest).pack(pady=2)
        tk.Button(menu, text="Sort Records", width=20, command=self.sort_records).pack(pady=2)
        tk.Button(menu, text="Add Student", width=20, command=self.add_student).pack(pady=2)
        tk.Button(menu, text="Delete Student", width=20, command=self.delete_student).pack(pady=2)
        tk.Button(menu, text="Update Student", width=20, command=self.update_student).pack(pady=2)

    # ---------- DISPLAY ----------

    # DISPLAY STUDENT DETAILS
    def show_students(self, students):
        self.output.delete(1.0, tk.END)
        total_percentage = 0

        for s in students:
            pct = get_percentage(s)
            total_percentage += pct

            # DISPLAY STUDENT INFO
            self.output.insert(tk.END,
                f"Name: {s['name']}\n"
                f"Student Number: {s['number']}\n"
                f"Coursework Total: {s['cw1'] + s['cw2'] + s['cw3']}\n"
                f"Exam Mark: {s['exam']}\n"
                f"Overall Percentage: {pct:.2f}%\n"
                f"Grade: {get_grade(pct)}\n"
                "---------------------------\n"
            )

        # DISPLAY SUMMARY
        if students:
            avg = total_percentage / len(students)
            self.output.insert(tk.END,
                f"Total Students: {len(students)}\n"
                f"Average Percentage: {avg:.2f}%"
            )

    # ---------- MENU FUNCTIONS ----------

    # VIEW ALL STUDENTS
    def view_all(self):
        self.show_students(self.students)

    # VIEW ONE STUDENT
    def view_one(self):
        num = simpledialog.askstring("Student", "Enter student number:")
        for s in self.students:
            if s['number'] == num:
                self.show_students([s])
                return
        messagebox.showinfo("Not Found", "Student not found")

    # HIGHEST MARK
    def highest(self):
        student = max(self.students, key=get_total)
        self.show_students([student])

    # LOWEST MARK
    def lowest(self):
        student = min(self.students, key=get_total)
        self.show_students([student])

    # SORT RECORDS (ASCENDING OR DESCENDING)
    def sort_records(self):
        order = simpledialog.askstring("Sort", "Enter 'A' for ascending or 'D' for descending:")
        if order is None:  # user cancelled
            return
        order = order.upper()
        if order == 'A':
            self.students.sort(key=get_total, reverse=False)
        elif order == 'D':
            self.students.sort(key=get_total, reverse=True)
        else:
            messagebox.showerror("Error", "Invalid input! Enter A or D.")
            return
        self.show_students(self.students)

    # ADD STUDENT
    def add_student(self):
        try:
            num = simpledialog.askstring("Add", "Student number:")
            name = simpledialog.askstring("Add", "Student name:")
            cw1 = int(simpledialog.askstring("Add", "Coursework 1:"))
            cw2 = int(simpledialog.askstring("Add", "Coursework 2:"))
            cw3 = int(simpledialog.askstring("Add", "Coursework 3:"))
            exam = int(simpledialog.askstring("Add", "Exam mark:"))

            self.students.append({
                "number": num,
                "name": name,
                "cw1": cw1,
                "cw2": cw2,
                "cw3": cw3,
                "exam": exam
            })
            write_file(self.students)
            self.view_all()
        except:
            messagebox.showerror("Error", "Invalid input")

    # DELETE STUDENT
    def delete_student(self):
        num = simpledialog.askstring("Delete", "Student number:")
        self.students = [s for s in self.students if s['number'] != num]
        write_file(self.students)
        self.view_all()

    # UPDATE STUDENT
    def update_student(self):
        num = simpledialog.askstring("Update", "Student number:")
        for s in self.students:
            if s['number'] == num:
                s['name'] = simpledialog.askstring("Update", "Name:", s['name'])
                s['cw1'] = int(simpledialog.askstring("Update", "Coursework 1:", s['cw1']))
                s['cw2'] = int(simpledialog.askstring("Update", "Coursework 2:", s['cw2']))
                s['cw3'] = int(simpledialog.askstring("Update", "Coursework 3:", s['cw3']))
                s['exam'] = int(simpledialog.askstring("Update", "Exam:", s['exam']))
                write_file(self.students)
                self.view_all()
                return
        messagebox.showinfo("Not Found", "Student not found")


# ---------- RUN PROGRAM ----------
root = tk.Tk()
app = StudentManager(root)
root.mainloop()
