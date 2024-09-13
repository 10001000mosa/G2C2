from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

# Home route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400

        # Process the uploaded file
        df = pd.read_csv(file)
        df['Total'] = df.select_dtypes(include='number').sum(axis=1)



        # Save the processed file to a BytesIO object
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)

        return send_file(output, mimetype='text/csv', as_attachment=True, attachment_filename='processed_data.csv')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)