
import tkinter as tk
from tkinter import ttk
import pygame

def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)  # Replace "your_audio_file.wav" with your .wav audio file path
    pygame.mixer.music.play()


def display_audio_bar(right_frame, audio_path):
    root = tk.Tk()
    root.title("Audio Player")

    # Function to toggle play/pause button
    def toggle_play():
        if play_button["text"] == "▶":
            play_button.config(text="⏸")
            play_audio()
            update_progress_bar()
        else:
            play_button.config(text="▶")
            pygame.mixer.music.pause()

    # Create play button
    play_button = ttk.Button(root, text="▶", command=toggle_play, style="Play.TButton")
    play_button.grid(row=0, column=0, pady=20)

    # Create progress bar
    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
    progress_bar.grid(row=0, column=1, padx=5, pady=20)

    # Styling the play button
    root.style = ttk.Style()
    root.style.configure("Play.TButton", font=("Helvetica", 20), width=4)

    # Function to update progress bar
    def update_progress_bar():
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            total_time = pygame.mixer.Sound(audio_path).get_length()
            progress = (current_time / total_time) * 100
            progress_bar["value"] = progress
            root.update()
            pygame.time.Clock().tick(10)  # Update every 10 milliseconds

    root.mainloop()

