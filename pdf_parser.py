import os
import pdfplumber
import camelot
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import shutil

def extract_text(pdf_path):
    """
    Extracts all text from a PDF file.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None
    return text

def extract_tables(pdf_path):
    """
    Extracts tables from a PDF file using camelot.
    Returns a list of tables, where each table is a list of lists (rows).
    """
    tables_data = []
    try:
        # 'lattice' is good for tables with clear grid lines
        # 'stream' is good for tables without clear lines, but might need more tuning
        tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice', suppress_stdout=True, line_scale=40)
        for table in tables:
            tables_data.append(table.df.values.tolist())

        # If lattice didn't find much, try stream
        if not tables_data or len(tables_data[0]) == 0 :
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream', suppress_stdout=True, edge_tol=500)
            for table in tables:
                tables_data.append(table.df.values.tolist())

    except Exception as e:
        print(f"Error extracting tables from {pdf_path} with camelot: {e}")
        # Fallback or alternative method could be added here if desired
    return tables_data

def extract_images_and_ocr(pdf_path, output_folder="extracted_images"):
    """
    Extracts images from a PDF, saves them, and performs OCR.
    Returns a list of OCR'd text from images.
    """
    images_text = []
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder) # Clean up old images
    os.makedirs(output_folder, exist_ok=True)

    try:
        images = convert_from_path(pdf_path, output_folder=output_folder, fmt='png', output_file="img_")
        image_files = sorted([os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith("img_")])

        for i, image_file_path in enumerate(image_files):
            try:
                # Ensure the file is indeed an image before trying to open
                if not image_file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
                    # pdf2image might save non-image files (like .ppm metadata files sometimes)
                    # We only want actual image files for OCR
                    if os.path.exists(image_file_path): # remove non-image files
                        os.remove(image_file_path)
                    continue

                text = pytesseract.image_to_string(Image.open(image_file_path))
                images_text.append({
                    "image_path": os.path.basename(image_file_path), # Return relative path for API response
                    "text": text.strip()
                })
            except pytesseract.TesseractNotFoundError:
                print("Pytesseract error: Tesseract is not installed or not in your PATH.")
                # Optionally re-raise or handle as a more critical error
                return {"error": "Tesseract not found."}
            except Exception as e:
                print(f"Error performing OCR on {image_file_path}: {e}")
                images_text.append({
                    "image_path": os.path.basename(image_file_path),
                    "text": f"Error during OCR: {e}"
                })
            finally:
                # Clean up the individual image file after OCR to save space,
                # as we are storing them in output_folder which is temporary for the request
                if os.path.exists(image_file_path):
                     os.remove(image_file_path)


    except Exception as e:
        print(f"Error extracting images from {pdf_path}: {e}")
        return {"error": f"Failed to extract images: {e}"}

    # Clean up the main image folder if it's empty or after processing
    if os.path.exists(output_folder) and not os.listdir(output_folder):
        os.rmdir(output_folder)

    return images_text

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    # Create a dummy PDF for testing if you don't have one.
    # This part requires a PDF file named 'sample.pdf' in the same directory.

    print("Note: For local testing, create a 'sample.pdf' in the current directory.")
    print("Or, ensure 'tesseract' and 'ghostscript' are installed and in PATH.")

    # You would need to create a sample.pdf for this test to run.
    # For now, we'll just print the functions.

    # test_pdf_path = "sample.pdf" # Replace with your test PDF
    # if not os.path.exists(test_pdf_path):
    #     print(f"{test_pdf_path} not found. Skipping local test.")
    # else:
    #     print(f"--- Extracting Text from {test_pdf_path} ---")
    #     extracted_text = extract_text(test_pdf_path)
    #     if extracted_text:
    #         print(extracted_text[:500] + "..." if extracted_text else "No text found.")

    #     print(f"\n--- Extracting Tables from {test_pdf_path} ---")
    #     extracted_tables = extract_tables(test_pdf_path)
    #     if extracted_tables:
    #         for i, table in enumerate(extracted_tables):
    #             print(f"Table {i+1}:")
    #             for row in table[:3]: # Print first 3 rows
    #                 print(row)
    #             if len(table) > 3:
    #                 print("...")
    #     else:
    #         print("No tables found or error during table extraction.")

    #     print(f"\n--- Extracting Images and OCR from {test_pdf_path} ---")
    #     ocr_results = extract_images_and_ocr(test_pdf_path, output_folder="test_extracted_images")
    #     if isinstance(ocr_results, dict) and "error" in ocr_results:
    #         print(f"Error in OCR: {ocr_results['error']}")
    #     elif ocr_results:
    #         for result in ocr_results:
    #             print(f"Image: {result['image_path']}, OCR Text: '{result['text'][:100]}...'")
    #     else:
    #         print("No images found or error during image extraction/OCR.")

    #     # Clean up test image folder
    #     if os.path.exists("test_extracted_images"):
    #         shutil.rmtree("test_extracted_images")
