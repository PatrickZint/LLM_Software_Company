import cv2
import numpy as np
import os


class ImageComparator:
    @staticmethod
    def load_image(image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_path}' not found.")
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to load image '{image_path}'. Unsupported format or corrupted file.")
        return image

    @staticmethod
    def compare_images(image_path1, image_path2, tolerance=10, highlight_color=(0, 0, 255), resize_strategy='error'):
        """
        Compare two images pixel-by-pixel and return a diff image highlighting the differences.

        If the image dimensions differ and resize_strategy is set to 'error', a ValueError is raised.
        """
        img1 = ImageComparator.load_image(image_path1)
        img2 = ImageComparator.load_image(image_path2)

        if img1.shape != img2.shape:
            if resize_strategy == 'error':
                raise ValueError("Images have different dimensions and resize_strategy is set to 'error'.")
            elif resize_strategy == 'resize':
                # Resize img2 to match img1's dimensions
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            else:
                raise ValueError(f"Unknown resize_strategy: {resize_strategy}")

        # Compute absolute difference between images
        diff = cv2.absdiff(img1, img2)
        # Convert difference to grayscale
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to identify significant differences
        _, thresh = cv2.threshold(gray, tolerance, 255, cv2.THRESH_BINARY)

        # Create a mask from the threshold image
        mask = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

        # Create a copy of the first image and highlight differences
        diff_image = img1.copy()
        # Where mask is not zero, overlay the highlight color
        diff_image[thresh != 0] = highlight_color

        # Additionally, you could compute a difference score
        difference_score = np.sum(thresh) / 255

        return diff_image, difference_score
