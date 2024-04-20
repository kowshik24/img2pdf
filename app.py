from flask import Flask, request, jsonify, send_file, render_template
import os
from werkzeug.utils import secure_filename
from src.utils import pdf_converter, transform_to_white

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/v1/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('files[]')
    if not uploaded_files:
        return jsonify({"error": "No files provided"})
    # remove all the previous files(.jpg, .jpeg, .png) from the uploads folder
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
    for file in uploaded_files:
        if file.filename == '':
            return jsonify({"error": "No selected file"})
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({"message": "Files uploaded successfully"})

@app.route('/v1/convert_to_pdf', methods=['GET'])
def convert_to_pdf():
    image_path = 'uploads'
    pdf_path = 'uploads/output.pdf'
    if not os.listdir(image_path):
        return jsonify({"error": "No images to convert"})

    pdf_path = pdf_converter(image_path, pdf_path)
    return send_file(pdf_path, as_attachment=True)

@app.route('/v1/transform_to_white', methods=['GET'])
def transform_to_white_endpoint():
    pdf_path = 'uploads/output.pdf'
    if not os.path.exists(pdf_path):
        return jsonify({"error": "PDF not found"})

    transformed_pdf_path = transform_to_white(pdf_path)
    return send_file(transformed_pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5110, debug=True)
