import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(m4a_file):
    # Load the M4A file
    sound = AudioSegment.from_file(m4a_file)
    
    # Export the audio to a temporary WAV file
    wav_file = "temp.wav"
    sound.export(wav_file, format="wav")
    
    # Use SpeechRecognition to perform speech-to-text
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
    
    # Convert speech to text
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Error: {e}"

