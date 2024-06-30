from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image

__all__ = ['preprocess_pdf']

def preprocess_pdf(file_path):
    # Converting the PDF to an image
    images = convert_from_path(file_path)
    image = images[0]

    # Converting the image to grayscale
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    # Thresholding the image to binary (black and white)
    _, binary_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Inverting the binary image (white text on black background)
    inverted_binary_image = cv2.bitwise_not(binary_image)

    # Detecting the coordinates of the text using the rotated rectangle
    coordinates = np.column_stack(np.where(inverted_binary_image > 0))
    angle = cv2.minAreaRect(coordinates)[-1]

    # Adjusting the angle of skew
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotating the image to correct the skew
    (height, width) = image.size
    center = (width // 2, height // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(np.array(image), rotation_matrix, (width, height))

    # Converting the rotated image to PIL format
    rotated_image_pil = Image.fromarray(rotated_image)
    
    return rotated_image_pil

