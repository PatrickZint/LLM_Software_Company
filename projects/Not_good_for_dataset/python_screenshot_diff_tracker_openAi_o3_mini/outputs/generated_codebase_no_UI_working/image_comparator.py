import cv2
import numpy as np


def compare_images(image_path1, image_path2, tolerance):
    """
    Compare two images at a pixel level and highlight differences.

    Args:
        image_path1 (str): Path to the first image.
        image_path2 (str): Path to the second image.
        tolerance (int): Threshold value to ignore minor differences.

    Returns:
        dict: Contains the annotated diff image, list of differences (bounding boxes), and image metadata.
    """
    # Load images using OpenCV
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)
    
    if img1 is None or img2 is None:
        raise ValueError('One of the images could not be loaded. Check the file paths.')

    # Verify that the dimensions match
    if img1.shape != img2.shape:
        raise ValueError('Images have different dimensions.')

    # Compute the absolute difference between images
    diff = cv2.absdiff(img1, img2)

    # Convert the difference to grayscale for thresholding
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get regions with significant differences
    _, thresh = cv2.threshold(gray, tolerance, 255, cv2.THRESH_BINARY)

    # Find contours of the differing areas
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    differences = []

    # Draw bounding rectangles around detected differences on a copy of the image
    annotated_image = img1.copy()
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        differences.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})
        cv2.rectangle(annotated_image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    metadata = {"width": img1.shape[1], "height": img1.shape[0]}
    
    return {"diff_image": annotated_image, "differences": differences, "metadata": metadata}
