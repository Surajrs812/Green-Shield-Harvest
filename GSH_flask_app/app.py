from flask import Flask, render_template, jsonify, send_file
import requests
import pandas as pd
import re
import os
from get_values import get_device_status  # Importing the function

app = Flask(__name__)

# Path to your Google Drive folder containing images
GOOGLE_DRIVE_FOLDER_URL = 'https://drive.google.com/drive/folders/10uNVya9tfD9WpX61lvrM2a6nY28hNGzH'  # Google Drive folder URL
DOWNLOAD_DIRECTORY = 'downloaded_images'  # Local directory to store images

# Ensure the download directory exists
os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)

# Function to get the file names and IDs from the Google Drive folder
def get_file_data_from_drive(folder_url):
    response = requests.get(folder_url)
    html_content = response.text

    # Regex pattern to find file links and titles
    file_links = re.findall(r'href="(/file/d/[^/]+)"', html_content)
    file_names = re.findall(r'title="(.*?)"', html_content)

    # Prepare a list of (file_name, file_id)
    file_data = [(name, link.split('/')[3]) for name, link in zip(file_names, file_links)]
    
    return file_data

# Function to download images using their file IDs
def download_images(file_data):
    for name, file_id in file_data:
        download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
        image_response = requests.get(download_url)
        
        if image_response.status_code == 200:
            file_path = os.path.join(DOWNLOAD_DIRECTORY, name)
            with open(file_path, 'wb') as f:
                f.write(image_response.content)

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for Raspberry Pi view
@app.route('/pi-view')
def pi_view():
    return render_template('pi_view.html')

# API to fetch sensor and weather data
@app.route('/get_device_status', methods=['GET'])
def get_status():
    data = get_device_status()  # Call the imported function
    print("Device Status Data:", data)
    return jsonify(data)

# Endpoint to download the dataset
@app.route('/download_dataset', methods=['GET'])
def download_dataset():
    output_csv = 'dataset.csv'
    
    # Get the list of file names from Google Drive
    file_data = get_file_data_from_drive(GOOGLE_DRIVE_FOLDER_URL)
    
    # Download images
    download_images(file_data)
    
    # Create DataFrame
    df = pd.DataFrame(file_data, columns=['File Name', 'File ID'])
    
    # Save the DataFrame to CSV
    df.to_csv(output_csv, index=False)
    
    # Send the CSV file for download
    return send_file(output_csv, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8000)