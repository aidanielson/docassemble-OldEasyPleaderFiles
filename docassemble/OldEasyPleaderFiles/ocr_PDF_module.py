__all__ = ['ocr_pdf']

from concurrent.futures import ThreadPoolExecutor
import subprocess
import tempfile
import os
from PIL import Image
import numpy as np
from pdf2image import convert_from_path
import cv2

# First Code Snippet Functions

def process_page(i, image_folder, pdf_file_path):
    base_image_name = f"page_{i + 1}"
    image_file_path = f"{image_folder}/{base_image_name}"
    subprocess.run(["pdftoppm", "-f", str(i + 1), "-l", str(i + 1), "-png", pdf_file_path, image_file_path])

    generated_files = [f for f in os.listdir(image_folder) if f.startswith(base_image_name)]
    if generated_files:
        generated_image_file_path = os.path.join(image_folder, generated_files[0])
        completed_process = subprocess.run(["tesseract", generated_image_file_path, "stdout", "--oem", "1", "-l", 'eng', "--psm", "11"], stdout=subprocess.PIPE)
        return completed_process.stdout.decode('utf-8')
    return ""

# Preprocessing function
def process_page_with_preprocessing(i, image_folder, pdf_file_path):
    base_image_name = f"page_{i + 1}"
    image_file_path = f"{image_folder}/{base_image_name}"
    subprocess.run(["pdftoppm", "-f", str(i + 1), "-l", str(i + 1), "-png", pdf_file_path, image_file_path])
    
    generated_files = [f for f in os.listdir(image_folder) if f.startswith(base_image_name)]
    if generated_files:
        generated_image_file_path = os.path.join(image_folder, generated_files[0])
        
        image = cv2.imread(generated_image_file_path, 0)
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        image = cv2.GaussianBlur(image, (5, 5), 0)
        
        processed_image_file_path = generated_image_file_path.replace(".png", "_processed.png")
        cv2.imwrite(processed_image_file_path, image)
        
        completed_process = subprocess.run(["tesseract", processed_image_file_path, "stdout", "--oem", "1", "-l", 'eng', "--psm", "11", 'OMP_THREAD_LIMIT', '1', 'quiet'], stdout=subprocess.PIPE)
        return completed_process.stdout.decode('utf-8')
    return ""

# Noise level testing function
def test_noise_level_on_all_pages(pdf_path, image_folder, threshold=1.75):  # added image_folder as a parameter
    images = convert_from_path(pdf_path, dpi=300)
    ocr_texts = []
    for page_number, image in enumerate(images):
        
        gray_image = Image.Image.convert(image, "L")
        np_gray_image = np.array(gray_image)
        
        cropped_area = np_gray_image[300:500, 0:200]
        
        noise_level = np.std(cropped_area)

        if noise_level > threshold:
            ocr_texts.append(process_page_with_preprocessing(page_number, image_folder, pdf_path))  # use image_folder
        else:
            ocr_texts.append(process_page(page_number, image_folder, pdf_path))  # use image_folder
    
    combined_text = '\f'.join(ocr_texts)
    return combined_text

# Main Operation with Parallel Execution
def ocr_pdf(pdf_file_path):
    with tempfile.TemporaryDirectory() as image_folder:
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(test_noise_level_on_all_pages, pdf_file_path, image_folder)  # pass image_folder as an argument
            result_text = future1.result()
    return result_text