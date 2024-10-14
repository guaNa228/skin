from image_manipulations import remove_bg, increase_contrast, detect_red_spots
from PIL import Image
import numpy as np
import cv2
from io import BytesIO


def process_image(img):
    # Creating two copies of images
    img = np.frombuffer(img, np.uint8)
    img2 = np.frombuffer(img, np.uint8)

    # Removing background
    image_no_bg = remove_bg(img)

    # Increasing contrast
    image_increased_contrast = increase_contrast(image_no_bg)

    # Detecting suspicious spots
    acne, areas = detect_red_spots(image_increased_contrast)

    # Converting images to RGB colorspace
    img, img2 = convertColor(img), convertColor(img2)

    # Drawing acne and pipmples contours on first image
    for red_spot in acne:
        cv2.drawContours(img, [red_spot], -1, (0, 0, 255), 2)

    # Drawing suspicious areas contours on second image
    for red_spot in areas:
        cv2.drawContours(img2, [red_spot], -1, (0, 255, 0), 2)

    return (to_bytearray(img), to_bytearray(img2))


def convertColor(img):
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


# Function to convert image from numpy array to byte array to pass it back to telegram bot
def to_bytearray(img):
    img = Image.fromarray(img)
    img_bytearray = BytesIO()
    img.save(img_bytearray, format='JPEG')
    img_bytearray = img_bytearray.getvalue()

    return img_bytearray
