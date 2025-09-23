import numpy as np
from PIL import Image
import cv2
import config


def compare_images(image1_path, image2_path, tolerance=config.DEFAULT_TOLERANCE):
    """
    Compare two images pixel-by-pixel.
    If image sizes differ, resize the second image to match the first.
    Returns a PIL Image object representing the diff image.
    Pixels that differ beyond the tolerance threshold are highlighted using DEFAULT_DIFF_COLOR.

    :param image1_path: File path for the first image.
    :param image2_path: File path for the second image.
    :param tolerance: Tolerance threshold for pixel differences.
    :return: PIL Image of the diff result.
    """
    try:
        # Load images using PIL and convert to RGB
        im1 = Image.open(image1_path).convert('RGB')
        im2 = Image.open(image2_path).convert('RGB')
    except Exception as e:
        raise ValueError(f"Error loading images: {e}")

    # If dimensions differ, resize im2 to match im1's size
    if im1.size != im2.size:
        im2 = im2.resize(im1.size)

    # Convert images to numpy arrays
    arr1 = np.array(im1).astype('int32')
    arr2 = np.array(im2).astype('int32')
    
    # Calculate absolute difference
    diff = np.abs(arr1 - arr2)

    # Create a mask where any channel difference exceeds the tolerance
    mask = np.any(diff > tolerance, axis=2)

    # Prepare an output image array
    # Where differences are found, we set the pixel to the diff color; otherwise, keep original
    diff_color = np.array(config.DEFAULT_DIFF_COLOR, dtype='uint8')
    output_arr = np.where(mask[:, :, None], diff_color, np.uint8(arr1))

    # Convert back to a PIL image
    diff_image = Image.fromarray(output_arr, 'RGB')
    return diff_image


if __name__ == "__main__":
    # For testing purposes only
    import sys
    if len(sys.argv) < 3:
        print("Usage: python image_comparator.py <image1> <image2>")
        sys.exit(1)
    diff_img = compare_images(sys.argv[1], sys.argv[2])
    diff_img.show()
