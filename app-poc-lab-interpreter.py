import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter.font as tkFont
from collections import Counter
from PIL import Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import seaborn as sns
import re
import matplotlib.pyplot as plt
import openai, os, requests
import PyPDF2
import speech_recognition as sr
from pdf2image import convert_from_path
from tkinter import filedialog
from tkinter import Tk
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter, legal
from PyPDF2 import PdfWriter, PdfReader
import tkinter as tk
from utils.lab_data_analysis import upload_pdf, generate_answer
import pygame
from tkinter import ttk
import pygame
from utils.process_image import upload_image
from utils.process_voice import audio_to_text
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image
import io

openai.api_type = os.environ.get("OPENAI_API_TYPE")
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = os.environ.get("OPENAI_API_VERSION")
# Azure OpenAI setup
openai.api_base = os.environ.get("OPENAI_API_BASE")
openai.api_key = os.environ.get("OPENAI_API_KEY")
deployment_id = os.environ.get("OPENAI_DEPLOYMENT_ID")


def verify_login(username, password, login_top_level, root):
    # Dummy authentication logic (replace with your own logic)
    if username == "admin" and password == "password":
        login_top_level.destroy()  # Close login window
        root.deiconify()  # Show the main window
    else:
        messagebox.showwarning("Login Failed", "Incorrect username or password")

def login_window(root):
    # Create a top-level window for the login
    login_top_level = tk.Toplevel(root)
    login_top_level.title("Login")
    login_top_level.geometry("300x150")
    login_top_level.grab_set()  # Makes the login window modal

    # Username Entry
    tk.Label(login_top_level, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_top_level)
    username_entry.pack()

    # Password Entry
    tk.Label(login_top_level, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_top_level, show="*")
    password_entry.pack()

    # Login Button
    login_button = tk.Button(login_top_level, text="Login", command=lambda: verify_login(username_entry.get(), password_entry.get(), login_top_level, root))
    login_button.pack(pady=10)

def on_enter(e, button, bg_color):
    button['background'] = bg_color

def on_leave(e, button, original_color):
    button['background'] = original_color


def get_dominant_color(image_path, num_colors=1):
    # Open the image
    image = Image.open(image_path)

    # Resize the image to reduce the number of pixels
    image = image.resize((100, 100))

    # Convert the image to RGB if it's not
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Get pixels and find the most common color
    pixels = list(image.getdata())
    most_common = Counter(pixels).most_common(num_colors)
    return most_common[0][0]  # Return the most dominant color

def close_app(root):
    root.destroy()

def find_files(directory):
    print(directory)
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(file)
            # Check for image files
            if file.endswith(".jpg") and "Imaging" in root:
                image_file = os.path.join(root, file)
                print(image_file)
            # Check for lab report PDF files
            elif file.endswith(".pdf") and "Lab_reports" in root:
                lab_file = os.path.join(root, file)
                print(lab_file)
            # Check for voice WAV files
            elif file.endswith(".wav") and "Voice_note" in root:
                voice_file = os.path.join(root, file)
                print(voice_file)

    return image_file, lab_file, voice_file

multimodal_text = None
lab_path = None
voice_text = None
chestxray = None
image_path = None
def upload_and_display_data(right_frame, right_bg_color):
    global multimodal_text
    global lab_path
    global chestxray
    global voice_text
    global image_path

    data_path = filedialog.askdirectory() #"../data/Patient_01/visit_05-04-2024"
    print(data_path)
    # Find files in the specified directory
    image_path, lab_path, voice_path = find_files(data_path)
    
    voice_text = audio_to_text(voice_path)
    # Upload PDF and get text and thumbnail
    chestxray, prediction = upload_image(image_path)
    print(prediction)
    pdf_text, lab_report_img = upload_pdf(lab_path)    
    multimodal_text = f"Lab Report: {pdf_text}\nVoice Transcript: {voice_text}\nChest X-ray prediction: {prediction}\n"
    print("multimodal text =--------------------------------------")
    print(multimodal_text)
    lab_report_image = ImageTk.PhotoImage(lab_report_img)

    # Create a nested frame for displaying elements side by side
    nested_frame = ttk.Notebook(right_frame)
    nested_frame.pack(pady=20)

    # Create tabs
    tab1 = tk.Frame(nested_frame)
    tab2 = tk.Frame(nested_frame)

    nested_frame.add(tab1, text="Lab Report")
    nested_frame.add(tab2, text="Chest X-Ray")

    # Display chest X-ray image
    chestxray = ImageTk.PhotoImage(chestxray)
    chestxray_label = tk.Label(tab2, image=chestxray)
    chestxray_label.pack(side=tk.LEFT, padx=20)

    # Plot the bar chart of the prediction
    plot_prediction(tab2, prediction)

    # Display lab report image
    lab_report_label = tk.Label(tab1, image=lab_report_image)
    lab_report_label.pack(side=tk.TOP, padx=20)

    # Display audio player
    display_audio_bar(tab1, voice_path, voice_text)

    # Pack the nested frame
    nested_frame.pack()

def show_transcript(voice_text):
    # Create a new window
    transcript_window = tk.Toplevel()
    transcript_window.title("Voice Transcript")

    # Create a Text widget to display the voice text
    transcript_text = tk.Text(transcript_window, wrap="word", height=20, width=50)
    transcript_text.insert(tk.END, voice_text)
    transcript_text.config(state=tk.DISABLED)  # Disable editing

    transcript_text.pack(fill=tk.BOTH, expand=True)

def plot_prediction(frame, prediction):
    # Sort the prediction dictionary by value in descending order
    sorted_prediction = sorted(prediction.items(), key=lambda x: x[1], reverse=False)[:10]
    labels, values = zip(*sorted_prediction)
     # Get the background color of tab2
    # Get the background color of tab2
    bg_color = frame.winfo_toplevel().tk.call(frame._w, "configure", "-background")[4]
    
    # Convert the color to an RGBA tuple
    bg_color_rgb = frame.winfo_toplevel().winfo_rgb(bg_color)
    bg_color_rgba = [x / 65535 for x in bg_color_rgb] + [1.0]

    fig, ax = plt.subplots(figsize=(3, 5), facecolor=bg_color_rgba)  # Adjust the figure size as needed
    bars = ax.barh(labels, values, color='lightblue', height=0.3)  # Set the bar color to light blue and height to 0.5
    ax.set_xlabel('Probability')
    ax.set_title('Prediction')
    ax.set_facecolor(bg_color_rgba)  # Set the background color of the plot

    # Add probability values next to the bars
    for bar, value in zip(bars, values):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value:.2f}', ha='left', va='center', fontsize=8)

    # Set custom x-axis ticks and labels
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(['0', '0.5', '1'])

    plt.tight_layout()

    # Convert the Matplotlib plot to a Tkinter-compatible image
    canvas = FigureCanvasTkAgg(fig, master=frame)
    # Set the background color of the canvas to match the background color of tab2
    canvas.get_tk_widget().config(background=bg_color)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT, padx=20, pady=20)

    plt.close(fig)  # Close the Matplotlib figure to avoid memory leaks


def play_audio(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)  # Replace "your_audio_file.wav" with your .wav audio file path
    pygame.mixer.music.play()


def display_audio_bar(right_frame, audio_path, voice_text):
    # Create a frame for the audio player
    audio_frame = tk.Frame(right_frame)
    audio_frame.pack(pady=20)

    # Function to toggle play/pause button
    def toggle_play():
        if play_button["text"] == "▶":
            play_button.config(text="⏸")
            play_audio(audio_path)
            update_progress_bar()
        else:
            play_button.config(text="▶")
            pygame.mixer.music.pause()

    # Create play button with ttk.Button and style
    play_button = ttk.Button(audio_frame, text="▶", command=toggle_play)
    play_button.grid(row=0, column=0, padx=5)

    # Create progress bar
    progress_bar = ttk.Progressbar(audio_frame, orient="horizontal", mode="determinate")
    progress_bar.grid(row=0, column=1, padx=5)

    # Function to update progress bar
    def update_progress_bar():
        while pygame.mixer.music.get_busy():
            current_time = pygame.mixer.music.get_pos() / 1000
            total_time = pygame.mixer.Sound(audio_path).get_length()
            progress = (current_time / total_time) * 100
            progress_bar["value"] = progress
            audio_frame.update()
            pygame.time.Clock().tick(10)

    # Create and add a clickable text link for transcript
    transcript_label = tk.Label(audio_frame, text="Transcribe", fg="blue", cursor="hand2")
    transcript_label.grid(row=0, column=2, padx=5)

    def show_transcript_window(event):
        show_transcript(voice_text)

    # Bind the label to show transcript window when clicked
    transcript_label.bind("<Button-1>", show_transcript_window)

    audio_frame.mainloop()


# Function to ask a question using Azure OpenAI's API
answer = None
def analyze_lab_result(multimodal_text, left_frame):
    global answer
    question = "Highligh any complains of the patients from the voice note, abnormal lab results with normal range for reference from lab report in bullet points, and high probability from chest X-ray prediction in one line. Give brief feedback for the patient (not using you) in bullet points like a 10-year experience doctor."
    print(multimodal_text)
    answer = generate_answer(question, multimodal_text, left_frame)
    message_label = tk.Label(left_frame, text=answer, fg='black', font=("Times New Roman", 10), wraplength=400)
    message_label.pack(pady=25)  # Place the label below the image


def download_sample_pdf():
    # Open the existing PDF
    existing_pdf = PdfReader(open(lab_path, "rb"))

    # Create a canvas with Reportlab for the text
    text_packet = io.BytesIO()
    text_canvas = canvas.Canvas(text_packet, pagesize=(22 * 72, 11 * 72))

    # Calculate the center coordinates of the page for the text
    center_x = letter[1] / 2 + 300
    center_y = letter[0] / 2 + 300

    # Split the answer text into lines
    lines = answer.split('\n')

    # Calculate the starting y-coordinate for the text to be centered vertically
    line_height = 12  # Adjust as needed
    total_height = len(lines) * line_height
    y_start = center_y + total_height / 2

    # Draw each line of text at the center of the page
    for line in lines:
        text_width = text_canvas.stringWidth(line)
        x_start = center_x - (text_width / 2)
        text_canvas.drawString(x_start, y_start, line)
        y_start -= line_height  # Move to the next line

    text_canvas.save()

    # Move to the beginning of the StringIO buffer for the text
    text_packet.seek(0)

    # Create a new PDF with Reportlab for the text
    text_pdf = PdfReader(text_packet)

    # Create a canvas with Reportlab for the image
    image_packet = io.BytesIO()
    image_canvas = canvas.Canvas(image_packet, pagesize=(22 * 72, 11 * 72))

    # Load the JPG image
    image = Image.open(image_path)
    image_width, image_height = image.size

    # Calculate the position to center the image on the page
    center_x_image = letter[1] / 2
    center_y_image = letter[0] / 2

    x_image_start = center_x_image - (image_width / 2)
    y_image_start = center_y_image - (image_height / 2)

    # Draw the image onto the canvas
    image_canvas.drawImage(image_path, x_image_start, y_image_start, width=image_width, height=image_height)
    image_canvas.save()

    # Move to the beginning of the StringIO buffer for the image
    image_packet.seek(0)

    # Create a new PDF with Reportlab for the image
    image_pdf = PdfReader(image_packet)

    # Create an output PDF writer
    output = PdfWriter()

    # Merge the output with the text PDF (on the first page)
    for text_page in text_pdf.pages:
        output.add_page(text_page)

    # Merge the existing PDF with the image PDF (on the last page)
    for page_number, page in enumerate(existing_pdf.pages):
        output.add_page(page)
        if page_number == len(existing_pdf.pages) - 1:
            for image_page in image_pdf.pages:
                output.add_page(image_page)

    # Save the modified PDF
    output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")],
                                                initialfile="modified_pdf")
    with open(output_path, 'wb') as output_file:
        output.write(output_file)
    print("Text and image added successfully. Modified PDF saved as:", output_path)

def main():
    root = tk.Tk()
    root.title("AI Clinical")
    root.geometry("800x600")
    #root.withdraw()  # Hide the root window

    # Initialize the login window
    login_window(root)
    
    # Styling options
    button_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
    button_bg = "#4a7abc"
    button_fg = "#ffffff"
    hover_color = "#36648b"
    left_bg_color = '#333333'
    # Get the dominant color from the logo    
    # Path to your logo image
    logo_path = 'logo/ai-clinical-note.png'  # Replace with your logo image path
    dominant_color = get_dominant_color(logo_path)
    right_bg_color = '#{:02x}{:02x}{:02x}'.format(*dominant_color)  # Convert RGB to hex
    # Create a frame for the right side elements (Logo and Buttons)
    right_frame = tk.Frame(root, bg=right_bg_color)
    right_frame.pack(side="right", fill="both", expand=True)
    
    # Create a frame for the left side elements (Image and Message)
    left_frame = tk.Frame(root)
    left_frame.pack(side="left", fill="both", expand=True)
    # Load the logo
    logo_image = Image.open(logo_path)
    logo_image.thumbnail((200, 200))  # Resize if necessary
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Display the logo
    logo_label = tk.Label(left_frame, image=logo_photo)
    logo_label.image = logo_photo
    logo_label.pack(pady=10)

    # Create a frame for the buttons
    button_frame = tk.Frame(left_frame)
    button_frame.pack(pady=5)

    # Upload Button
    upload_button = tk.Button(button_frame, text="Upload", font=button_font, bg=button_bg, fg=button_fg, relief="raised", borderwidth=2, command=lambda: upload_and_display_data(right_frame, right_bg_color))
    upload_button.pack(side="left", padx=5)
    upload_button.bind("<Enter>", lambda e: on_enter(e, upload_button, hover_color))
    upload_button.bind("<Leave>", lambda e: on_leave(e, upload_button, button_bg))


    # Analyze Button
    analyze_button = tk.Button(button_frame, text="Analyze", font=button_font, bg=button_bg, fg=button_fg, relief="raised", borderwidth=2, command=lambda: analyze_lab_result(multimodal_text, left_frame))
    analyze_button.pack(side="left", padx=5)
    analyze_button.bind("<Enter>", lambda e: on_enter(e, analyze_button, hover_color))
    analyze_button.bind("<Leave>", lambda e: on_leave(e, analyze_button, button_bg))

    # Close Button
    close_button = tk.Button(button_frame, text="Close", font=button_font, bg=button_bg, fg=button_fg, relief="raised", borderwidth=2, command=lambda: close_app(root))
    close_button.pack(side="left", padx=5)
    close_button.bind("<Enter>", lambda e: on_enter(e, close_button, hover_color))
    close_button.bind("<Leave>", lambda e: on_leave(e, close_button, button_bg))

    # Label for the final message
    message_label = tk.Label(left_frame, text="Upload a pdf report to analyze the result", fg='black', font=("Helvetica", 12))
    message_label.pack(pady=2)

    # Create a frame for the download button
    download_frame = tk.Frame(left_frame)
    download_frame.pack(side="bottom", pady=(0, 20))  # Pack it to the bottom of the left_frame

    # Download Button
    download_button = tk.Button(download_frame, text="Download Interpreted Lab Report", font=button_font, bg=button_bg, fg=button_fg, relief="raised", borderwidth=2, command=download_sample_pdf)
    download_button.pack(side="bottom", padx=5)  # Pack it to the bottom of download_frame
    download_button.bind("<Enter>", lambda e: on_enter(e, download_button, hover_color))
    download_button.bind("<Leave>", lambda e: on_leave(e, download_button, button_bg))

    root.mainloop()

if __name__ == "__main__":
    main()