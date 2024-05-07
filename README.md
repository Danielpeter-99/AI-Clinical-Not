# AI-Clinical-Assistant
AI Clinical Assistant for Microsoft AI Hackathon 2024

## Demo

https://github.com/Danielpeter-99/AI-Clinical-Note/assets/70642181/295ce6bf-cc31-4a94-8552-0b9065ad77fc

**This application, coded in Python with Tkinter for the GUI, appears to be an interface named "AI Clinical". The key features and functionalities are as follows:**

- Login System: It has a simple login system where users can enter a username and password. The login is verified against preset credentials (in this case, 'admin' and 'password'). After successful login, the user is directed to the main window of the application.

- File Upload and Display: Users can upload a file, likely of a consult note, lab results. The uploaded file is then displayed in the GUI.

- File Analysis: The core feature of the application is analyzing the uploaded file to interpret the lab report together with the voice note and chest x-ray. It uses a generative AI model from OpenAI (OpenAI GPT-4) to process the file and extract text information.

- Data Visualization: After analysis, the application generates a summary of the studies, as well as highlighting important details that might be of concern.

- Download interpreted lab reports: The user has option to download lab reports with AI-generated notes.

- Interactive GUI Components: The GUI includes interactive elements like buttons for uploading files, analyzing them, and closing the application. These buttons change color when hovered over, enhancing user experience.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_API_TYPE`

`OPENAI_API_VERSION`

`OPENAI_API_BASE`

`OPENAI_API_KEY`

`OPENAI_DEPLOYMENT_ID`

## Installation

Install the required packages using pip

```bash
pip install -r requirements.txt
```

Once the environment variables setup, the file may be ran using


```bash
python lab-report-interpreter.py
```

## License

[Apache-2.0](https://github.com/Danielpeter-99/AI-Clinical-Note?tab=Apache-2.0-1-ov-file#readme)

