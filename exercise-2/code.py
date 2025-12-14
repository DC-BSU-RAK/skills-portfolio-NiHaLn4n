import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import random
import os

# Path to background image
IMAGE_PATH = "exercise-2\joke.jpg"

# Path to jokes file
JOKE_FILE  = "exercise-2\Jokes.txt"

# Window size
WINDOW_SIZE = (800, 600)

# Blur intensity
BLUR_RADIUS = 12


# Load jokes from file
def load_jokes(path):
    # List to store jokes
    jokes = []

    # If file doesn't exist, return empty list
    if not os.path.exists(path):
        return jokes

    # Read file line by line
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            # Split setup and punchline
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline.strip()))

    return jokes


# Make blurred background image
def make_blurred_background(img_path, size, blur_radius):
    # Open and convert to RGBA
    img = Image.open(img_path).convert("RGBA")

    target_w, target_h = size
    src_w, src_h = img.size

    # Scale image to fill window
    scale = max(target_w / src_w, target_h / src_h)
    img = img.resize((int(src_w * scale), int(src_h * scale)), Image.LANCZOS)

    # Crop center area to fit window
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    img = img.crop((left, top, left + target_w, top + target_h))

    # Apply blur
    img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return img


# Joke Application
class JokeApp:
    def __init__(self, root):
        # Setup window
        self.root = root
        self.root.title("Alexa Joke Assistant")
        self.root.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")
        self.root.resizable(False, False)

        # Load jokes
        self.jokes = load_jokes(JOKE_FILE)
        self.current = ("", "")  # Store current joke

        # Create canvas for background
        self.canvas = tk.Canvas(root, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Prepare blurred background
        blurred = make_blurred_background(IMAGE_PATH, WINDOW_SIZE, BLUR_RADIUS)

        # Add transparent orange overlay
        overlay = Image.new("RGBA", WINDOW_SIZE, (255, 165, 0, 70))
        blurred = Image.alpha_composite(blurred, overlay)

        # Convert for Tkinter
        self.bg_img = ImageTk.PhotoImage(blurred)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        # Button to get a joke
        self.title_btn = tk.Button(
            root, text="Alexa tell me a Joke",
            font=("Helvetica", 20, "bold"),
            bg="#2AA6A6", fg="white",
            activebackground="#218A8A",
            width=20,
            command=self.new_joke
        )
        self.canvas.create_window(WINDOW_SIZE[0] // 2, 70, window=self.title_btn)

        # Joke setup text
        self.setup_var = tk.StringVar(value="")
        self.setup_label = tk.Label(
            root, textvariable=self.setup_var,
            font=("Helvetica", 26, "bold"),
            fg="black",
            wraplength=700,
            justify="center"
        )
        self.canvas.create_window(WINDOW_SIZE[0] // 2, 220, window=self.setup_label)

        # Punchline text
        self.punch_var = tk.StringVar(value="")
        self.punch_label = tk.Label(
            root, textvariable=self.punch_var,
            font=("Helvetica", 20, "italic"),
            fg="#003366",
            wraplength=700,
            justify="center"
        )
        self.canvas.create_window(WINDOW_SIZE[0] // 2, 300, window=self.punch_label)

        # Button to show punchline
        self.show_btn = tk.Button(
            root, text="Show Punchline", width=20,
            bg="#2AA6A6", fg="white",
            command=self.show_punchline
        )
        self.canvas.create_window(WINDOW_SIZE[0] // 2, 380, window=self.show_btn)

        # Button for next joke
        self.next_btn = tk.Button(
            root, text="Next Joke", width=20,
            bg="#2AA6A6", fg="white",
            command=self.new_joke
        )
        self.canvas.create_window(WINDOW_SIZE[0] // 2, 450, window=self.next_btn)

        # Quit button
        self.quit_btn = tk.Button(
            root, text="Quit", width=20,
            bg="#2AA6A6", fg="white",
            command=root.destroy
        )
        self.canvas.create_window(WINDOW_SIZE[0] // 2, 520, window=self.quit_btn)

        # Load first joke
        self.new_joke()

    # Pick a new joke
    def new_joke(self):
        # If no jokes found
        if not self.jokes:
            self.setup_var.set("No jokes found in file!")
            return

        # Clear punchline
        self.punch_var.set("")

        # Choose a random joke
        self.current = random.choice(self.jokes)

        # Display setup
        self.setup_var.set(self.current[0])

    # Show punchline
    def show_punchline(self):
        if self.current:
            self.punch_var.set(self.current[1])


# Run app
root = tk.Tk()
app = JokeApp(root)
root.mainloop()
