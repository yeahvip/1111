import os
import tempfile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import uuid

from pdf_parser import extract_text, extract_tables, extract_images_and_ocr

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir() # Use system temp directory for uploads
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/parse_pdf', methods=['POST'])
def parse_pdf_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file or not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Please upload a PDF."}), 400

    filename = secure_filename(file.filename)
    # Create a unique temporary file to save the upload
    temp_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")

    try:
        file.save(temp_pdf_path)

        # Prepare a folder for images extracted from this specific PDF
        # This folder will be created and managed by extract_images_and_ocr
        unique_image_folder_name = f"extracted_images_{uuid.uuid4()}"
        # We pass the base path for image folders, pdf_parser will create the unique one inside it.
        # For simplicity, let's use a subfolder in the temp directory.
        base_image_output_folder = os.path.join(app.config['UPLOAD_FOLDER'], unique_image_folder_name)

        # Process the PDF
        text_content = extract_text(temp_pdf_path)
        table_content = extract_tables(temp_pdf_path)
        # The extract_images_and_ocr function will handle image saving and cleanup
        image_ocr_results = extract_images_and_ocr(temp_pdf_path, output_folder=base_image_output_folder)

        results = {
            "filename": filename,
            "text": text_content,
            "tables": table_content,
            "image_ocr_results": image_ocr_results
        }

        return jsonify(results), 200

    except Exception as e:
        # Log the exception e
        app.logger.error(f"Error processing file {filename}: {e}")
        return jsonify({"error": f"An error occurred while processing the PDF: {str(e)}"}), 500
    finally:
        # Clean up the uploaded PDF file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)
        # The image folder is cleaned by extract_images_and_ocr itself or can be cleaned here too if needed.
        # if os.path.exists(base_image_output_folder): # This was handled by the function
        #     shutil.rmtree(base_image_output_folder)


if __name__ == '__main__':
    # Ensure Tesseract and Ghostscript are available in PATH for the underlying libraries to work.
    print("Starting Flask server. Ensure Tesseract OCR and Ghostscript are installed and in your PATH.")
    app.run(debug=True, host='0.0.0.0', port=5000)
