import cv2
import cvzone
import numpy as np
from cvzone.SelfiSegmentationModule import SelfiSegmentation

segmentor = SelfiSegmentation()

# Removing background using SelfiSegmentation


def remove_bg(img):
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    green = (0, 255, 0)
    img_no_bg = segmentor.removeBG(img, cutThreshold=0.45)
    return img_no_bg


# Increasing contrast with CLAHE on lab colorspace
def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(5, 5))
    cl = clahe.apply(l)
    updated_lab = cv2.merge((cl, a, b))
    updated_image = cv2.cvtColor(updated_lab, cv2.COLOR_LAB2BGR)
    return updated_image


def detect_red_spots(image):
    # Converting image to HSV colorspace
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Lower Hue settings
    lower_red = np.array([0, 120, 100])
    upper_red = np.array([15, 230, 230])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # Higher Hue settings
    lower_red = np.array([130, 120, 100])
    upper_red = np.array([180, 230, 230])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)

    # Mask merging
    mask = mask1 + mask2

    # Removing noise and merging close contours
    kernel = cv2.getStructuringElement(cv2.MORPH_OPEN, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Finding the exact contours
    contours, _ = cv2.findContours(
        mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Dividing contours onto 2 types depending on their size: acne and pipmples and damaged areas
    acne = []
    damaged_areas = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 50:
            if area > 1000:
                damaged_areas.append(contour)
            else:
                acne.append(contour)
    return (acne, damaged_areas)
