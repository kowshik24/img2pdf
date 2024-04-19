from PIL import Image
import fitz # PyMuPDF
import os
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def pdf_converter(image_folder, pdf_path):
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_files:
        return None # Return None or raise an exception if no images found

    doc = fitz.open() # Create a new PDF document

    for img_file in image_files:
        img_path = os.path.join(image_folder, img_file)
        img = Image.open(img_path)
        img.load()
        img.save(img_path) # Save the image in its current format, ensuring it's accessible

        # Convert the image to a PDF
        img_pdf = fitz.open(img_path) # This opens the image as a PDF document
        rect = img_pdf[0].rect # Get the dimensions of the image
        pdf_page = doc.new_page(width=rect.width, height=rect.height) # Create a new page
        # Insert the image into the PDF page
        pdf_page.insert_image(pdf_page.rect, filename=img_path, keep_proportion=True)

    doc.save(pdf_path) # Save the new PDF document
    return pdf_path




def transform_to_white(pdf_path):
    transformed_pdf_path = pdf_path.replace(".pdf", "_white.pdf")
    doc = fitz.open(pdf_path)

    for page in doc:
        rect = page.rect
        page.insert_rectangle(rect, color=(1, 1, 1), fill_opacity=1)  # Cover the page with a white rectangle

    doc.save(transformed_pdf_path)
    return transformed_pdf_path



