from flask import Flask, render_template, request, send_file
import os
from file_processor import process_file  # Import the processing function

# Define the Flask app
app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

# Create the directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Call the process_file function from file_processor.py
        processed_filepath = process_file(filepath)
        
        if processed_filepath:
            return send_file(processed_filepath, as_attachment=True)
        else:
            return 'Error processing file', 500
    return 'Invalid file format', 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=8001)