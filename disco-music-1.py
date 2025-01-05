import os
import tkinter as tk
from tkinter import filedialog
from pygame import mixer
from ttkbootstrap import Style
from PIL import Image, ImageTk
import random

# Initialize Pygame mixer
mixer.init()

# Functions
def toggle_play_pause():
    """Toggle between playing and pausing the music."""
    global is_playing
    if not current_song:
        return
    if is_playing:
        mixer.music.pause()
        status_label.config(text="Paused")
        play_pause_button.config(image=play_icon)
        is_playing = False
    else:
        mixer.music.unpause()
        status_label.config(text="Playing")
        play_pause_button.config(image=pause_icon)
        is_playing = True

def next_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index + 1) % len(playlist)
        load_song()

def previous_song():
    global current_song_index
    if playlist:
        current_song_index = (current_song_index - 1) % len(playlist)
        load_song()

def load_song():
    global current_song, is_playing
    current_song = playlist[current_song_index]
    mixer.music.load(current_song)
    mixer.music.play()
    is_playing = True
    play_pause_button.config(image=pause_icon)
    status_label.config(text="Playing")
    song_label.config(text=f"Now Playing: {os.path.basename(current_song)}")

def open_files():
    global playlist, current_song_index
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if files:
        playlist = list(files)
        current_song_index = 0
        load_song()

def disco_light_effect():
    """Change the background color periodically to simulate a disco light effect."""
    color = random.choice(["#FF5733", "#33FF57", "#3357FF", "#FF33A8", "#A833FF", "#33FFF3", "#AF0000", "#5F87FF", "#FF0000", "#D7D700", "#875FFF"])
    root.configure(bg=color)
    
    # Update the background color of text labels to match the disco background color
    status_label.config(bg=color)
    song_label.config(bg=color)
    control_frame.config(bg=color)

    root.after(500, disco_light_effect)  # Change color every 500 milliseconds

def animate_gif(index):
    """Animate the GIF by updating the image frame."""
    frame = gif_frames[index]
    image_label.config(image=frame)
    next_index = (index + 1) % len(gif_frames)  # Loop through frames
    root.after(100, animate_gif, next_index)  # Adjust the speed as needed (100ms)

# GUI Setup with ttkbootstrap
root = tk.Tk()
root.title("PK's Music Player")
root.geometry("530x550")

# Apply theme
style = Style(theme="cosmo")  # Choose from many themes like "cosmo", "flatly", etc.
root.configure(bg=style.colors.bg)

playlist = []
current_song = None
current_song_index = 0
is_playing = False

# Load icons
open_icon = tk.PhotoImage(file="C:/PYTHON/Project/open_icon.png")
play_icon = tk.PhotoImage(file="C:/PYTHON/Project/play_icon.png")
pause_icon = tk.PhotoImage(file="C:/PYTHON/Project/pause_icon.png")
prev_icon = tk.PhotoImage(file="C:/PYTHON/Project/prev_icon.png")
next_icon = tk.PhotoImage(file="C:/PYTHON/Project/next_icon.png")

# Load and process GIF
gif_path = "C:/PYTHON/Project/disco_image.gif"  # Replace with your GIF path
gif_image = Image.open(gif_path)

# Convert all frames to RGBA and store them
gif_frames = []
try:
    while True:
        frame = gif_image.copy().convert("RGBA")  # Ensure compatibility
        gif_frames.append(ImageTk.PhotoImage(frame))
        gif_image.seek(gif_image.tell() + 1)
except EOFError:
    pass  # End of GIF frames

# UI Elements
image_label = tk.Label(root, bg=style.colors.bg)
image_label.grid(row=0, column=0, columnspan=5, pady=10)

status_label = tk.Label(root, text="Welcome, Let's play music....", font=("Helvetica", 12, "bold"), fg=style.colors.info, bg=style.colors.bg)
status_label.grid(row=1, column=0, columnspan=5, pady=10)

song_label = tk.Label(root, text="No song loaded !!", font=("Helvetica", 10, "italic"), fg=style.colors.success, bg=style.colors.bg)
song_label.grid(row=2, column=0, columnspan=5)

control_frame = tk.Frame(root, bg=style.colors.bg)
control_frame.grid(row=3, column=0, columnspan=5, pady=10)

open_button = tk.Button(control_frame, image=open_icon, command=open_files, bg=style.colors.primary, borderwidth=0)
open_button.grid(row=0, column=0, padx=1)

prev_button = tk.Button(control_frame, image=prev_icon, command=previous_song, bg=style.colors.primary, borderwidth=0)
prev_button.grid(row=0, column=1, padx=1)

play_pause_button = tk.Button(control_frame, image=play_icon, command=toggle_play_pause, bg=style.colors.primary, borderwidth=0)
play_pause_button.grid(row=0, column=2, padx=1)

next_button = tk.Button(control_frame, image=next_icon, command=next_song, bg=style.colors.primary, borderwidth=0)
next_button.grid(row=0, column=3, padx=1)

# Start the GIF animation and disco light effect
animate_gif(0)
disco_light_effect()

# Run the application
root.mainloop()
