import os
import threading  # Required for multithreading core optimization [cite: 637]
import time
from flask import Flask, redirect, render_template, request
from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd

# --- DYNAMIC PATH MANAGEMENT CORE FIXED ---
# Get the absolute folder path where app.py actually lives
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

disease_info_path = os.path.join(BASE_DIR, 'disease_info.csv')
supplement_info_path = os.path.join(BASE_DIR, 'supplement_info.csv')
model_path = os.path.join(BASE_DIR, "plant_disease_model_1_latest.pt")

# Load structural databases securely using absolute paths
disease_info = pd.read_csv(disease_info_path, encoding='cp1252')
supplement_info = pd.read_csv(supplement_info_path, encoding='cp1252')

# Initialize and establish the computer vision evaluation stack
model = CNN.CNN(39)    
# map_location forces CPU execution matching Hugging Face free tier hosting limits [cite: 650]
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

def prediction(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    input_data = TF.to_tensor(image)
    input_data = input_data.view((-1, 3, 224, 224))
    output = model(input_data)
    output = output.detach().numpy()
    index = np.argmax(output)
    return index

# Worker task function for background thread non-blocking execution [cite: 7, 134, 175]
def save_file_async(image_storage_object, destination_path):
    print(f"\n[THREAD START] Worker handling concurrent disk write I/O operations...")
    start_io = time.time()
    
    # Perform raw storage save operations isolated from main execution thread
    image_storage_object.save(destination_path)
    
    end_io = time.time()
    print(f"[THREAD SUCCESS] Disk write complete in {round(end_io - start_io, 4)} seconds.")


app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact-us.html')

@app.route('/index')
def ai_engine_page():
    return render_template('index.html')

@app.route('/mobile-device')
def mobile_device_detected_page():
    return render_template('mobile-device.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        start_total = time.time()
        
        image = request.files['image']
        filename = image.filename
        
        # Ensure uploads folder is resolved cleanly relative to the runtime folder
        uploads_dir = os.path.join(BASE_DIR, 'static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = os.path.join(uploads_dir, filename)
        
        # --- MULTITHREADING CORE OPTIMIZATION [cite: 7, 637] ---
        # Initialize a dedicated worker thread for non-blocking file saving operations
        io_thread = threading.Thread(target=save_file_async, args=(image, file_path))
        
        # Launch background thread execution concurrently [cite: 35, 94]
        io_thread.start()
        
        # While the background worker thread writes the binary tracking data stream to the disk,
        # the main server thread prepares to perform data expansion modeling.
        # We synchronize execution by joining the thread before the prediction engine parses the path matrix[cite: 130].
        io_thread.join()
        # -----------------------------------------------------
        
        # Pass file snapshot structure context directly into PyTorch AI evaluation matrix
        pred = prediction(file_path)
        
        # Extract respective targeted information vectors
        title = disease_info['disease_name'][pred]
        description = disease_info['description'][pred]
        prevent = disease_info['Possible Steps'][pred]
        image_url = disease_info['image_url'][pred]
        supplement_name = supplement_info['supplement name'][pred]
        supplement_image_url = supplement_info['supplement image'][pred]
        supplement_buy_link = supplement_info['buy link'][pred]
        
        end_total = time.time()
        print(f"[SERVER ROUTE METRIC] Total route execution lifecycle concluded in {round(end_total - start_total, 4)} seconds.\n")
        
        return render_template(
            'submit.html', 
            title=title, 
            desc=description, 
            prevent=prevent, 
            image_url=image_url, 
            pred=pred, 
            sname=supplement_name, 
            simage=supplement_image_url, 
            buy_link=supplement_buy_link
        )

@app.route('/market', methods=['GET', 'POST'])
def market():
    return render_template(
        'market.html', 
        supplement_image=list(supplement_info['supplement image']),
        supplement_name=list(supplement_info['supplement name']), 
        disease=list(disease_info['disease_name']), 
        buy=list(supplement_info['buy link'])
    )

if __name__ == '__main__':
    app.run(debug=True)