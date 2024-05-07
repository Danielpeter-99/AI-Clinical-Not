import os

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

directory = "../data/Patient_01/Visit_05-04-2024"
image_file, lab_file, voice_file = find_files(directory)