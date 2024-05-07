import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import openai
import PyPDF2


def upload_pdf(pdf_path):
    print("pdf path ---------------")
    print(pdf_path)
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
        pdf_text = text

    file_path = "data/Patient_01/Visit_05-04-2024/Lab_reports/lab-report.jpg"
    if file_path:
        original_image = Image.open(file_path)
        thumbnail = original_image.copy()
        thumbnail.thumbnail((900, 900))  # Resize the image for display
    
    return pdf_text, thumbnail
    
def generate_answer(question, text, left_frame):
        #print(question)
    prompt = [{"role": "user", "content": f"Question: {question}\nContext: {text}\nAnswer:"}]

    # Set parameters for the completion
    params = {
        "temperature": 0.5,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop": ["\n"]
    }

    completion = openai.ChatCompletion.create(
    messages=prompt,
    deployment_id="gpt-4",
    )

    # Extract and return the answer
    answer = completion.choices[0].message["content"]
    
    return answer