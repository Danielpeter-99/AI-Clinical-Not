import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox
import openai
import PyPDF2
import torchxrayvision as xrv
import skimage, torch, torchvision
import numpy as np

def predict_image(img):
    img = np.array(img)
    img = xrv.datasets.normalize(img, 255) # convert 8-bit image to [-1024, 1024] range
    img = img.mean(2)[None, ...] # Make single color channel

    transform = torchvision.transforms.Compose([xrv.datasets.XRayCenterCrop(),xrv.datasets.XRayResizer(224)])

    img = transform(img)
    img = torch.from_numpy(img)

    # Load model and process image
    model = xrv.models.DenseNet(weights="densenet121-res224-all")
    outputs = model(img[None,...]) # or model.features(img[None,...]) 
    print(outputs.shape)
    # Print results
    result = dict(zip(model.pathologies,outputs[0].detach().numpy()))
    return result

def upload_image(image_path):
    if image_path:
        original_image = Image.open(image_path)
        prediction = predict_image(original_image)
        thumbnail = original_image.copy()
        thumbnail.thumbnail((700, 700))  # Resize the image for display
        
    return thumbnail, prediction
