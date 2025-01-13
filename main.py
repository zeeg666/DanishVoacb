import os
import random
import tkinter as tk
from tkinter import ttk
import pygame
from excel_flipcard import get_translation_and_sentence

# Initialize pygame mixer for playing audio
pygame.mixer.init()

# Load all mp3 files from the "General" folder
folder_path = "General"
mp3_files = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
mp3_files.sort()  # Ensure files are sorted alphabetically

# Application state
current_index = 0
random_mode = False
flip_mode = False

# Function to update displayed word
def update_word_label():
    word_label.config(text=mp3_files[current_index].replace(".mp3", ""))

# Function to play the current word pronunciation
def play_word():
    pygame.mixer.music.load(os.path.join(folder_path, mp3_files[current_index]))
    pygame.mixer.music.play()

# Function to go to the next word
def next_word():
    global current_index
    if random_mode:
        current_index = random.randint(0, len(mp3_files) - 1)
    else:
        current_index = (current_index + 1) % len(mp3_files)
    update_word_label()
    sentence_label.config(text="")

# Function to go to the previous word
def prev_word():
    global current_index
    if random_mode:
        current_index = random.randint(0, len(mp3_files) - 1)
    else:
        current_index = (current_index - 1) % len(mp3_files)
    update_word_label()
    sentence_label.config(text="")

# Function to toggle random mode
def toggle_random_mode():
    global random_mode
    random_mode = not random_mode
    mode_button.config(text="Mode: Random" if random_mode else "Mode: Ordered")

# Function to toggle flip card mode
def toggle_flip_card():
    global flip_mode
    flip_mode = not flip_mode
    if flip_mode:
        word = mp3_files[current_index].replace(".mp3", "")
        translation, sentence = get_translation_and_sentence(word)
        if translation and sentence:
            word_label.config(text=f"{translation}")
            sentence_label.config(text=f"{sentence}", font=("Arial", 14))
        elif translation:
            word_label.config(text=f"{translation}")
            sentence_label.config(text="")
        else:
            word_label.config(text="Translation not found")
            sentence_label.config(text="")
    else:
        update_word_label()
        sentence_label.config(text="")

# Function to handle keyboard input
def handle_keypress(event):
    if event.keysym == "Left":
        prev_word()
    elif event.keysym == "Right":
        next_word()
    elif event.keysym == "s":
        play_word()
    elif event.keysym == "space":
        toggle_flip_card()

# Create the main window
root = tk.Tk()
root.title("Danish Pronunciation Practice")
root.geometry("800x250")

# Bind keyboard events
root.bind("<Left>", handle_keypress)
root.bind("<Right>", handle_keypress)
root.bind("s", handle_keypress)
root.bind("<space>", handle_keypress)

# Word label
word_label = tk.Label(root, text="", font=("Arial", 24), pady=20)
word_label.pack()

# Sentence label
sentence_label = tk.Label(root, text="", font=("Arial", 14), pady=10)
sentence_label.pack()

# Navigation buttons
button_frame = tk.Frame(root)
button_frame.pack()

prev_button = tk.Button(button_frame, text="Previous", command=prev_word, width=10)
prev_button.grid(row=0, column=0, padx=5)

speak_button = tk.Button(button_frame, text="Speak", command=play_word, width=10)
speak_button.grid(row=0, column=1, padx=5)

next_button = tk.Button(button_frame, text="Next", command=next_word, width=10)
next_button.grid(row=0, column=2, padx=5)

# Mode toggle button
mode_button = tk.Button(root, text="Mode: Ordered", command=toggle_random_mode, width=15)
mode_button.pack(pady=10)

# Flip card button
flip_button = tk.Button(root, text="Flip Card", command=toggle_flip_card, width=15)
flip_button.pack(pady=10)

# Initialize the first word
update_word_label()

# Run the application
root.mainloop()
