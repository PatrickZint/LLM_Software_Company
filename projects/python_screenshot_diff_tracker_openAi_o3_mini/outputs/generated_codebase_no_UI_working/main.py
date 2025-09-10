import argparse
import os
import sys
import logging
import yaml
import cv2
from datetime import datetime

from image_comparator import compare_images
from database import init_db, insert_comparison_record
from logger_config import setup_logger


def load_config(config_path):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config


def main():
    parser = argparse.ArgumentParser(description='Compare two images and store diff results.')
    parser.add_argument('image1', help='Path to the first image file.')
    parser.add_argument('image2', help='Path to the second image file.')
    parser.add_argument('--config', default='config.yaml', help='Path to the configuration YAML file.')
    args = parser.parse_args()

    config = load_config(args.config)

    # Set up logging
    setup_logger(config.get('logging', {}))
    logger = logging.getLogger(__name__)
    
    # Validate that the input image formats are supported
    supported_formats = config.get('image', {}).get('supported_formats', ['png', 'jpg', 'jpeg'])
    ext1 = os.path.splitext(args.image1)[1][1:].lower()
    ext2 = os.path.splitext(args.image2)[1][1:].lower()
    if ext1 not in supported_formats or ext2 not in supported_formats:
        logger.error('Unsupported image format. Supported formats: %s', supported_formats)
        sys.exit(1)

    # Ensure export directory exists
    export_dir = config.get('export', {}).get('path', 'exported_diffs')
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)
        logger.info('Created export directory: %s', export_dir)

    try:
        # Get tolerance threshold from config
        tolerance = config.get('image', {}).get('threshold', 30)
        # Compare images
        result = compare_images(args.image1, args.image2, tolerance)
        diff_image = result['diff_image']
        differences = result['differences']
        metadata = result['metadata']
    except Exception as e:
        logger.exception('Error during image comparison: %s', e)
        sys.exit(1)

    # Save the annotated diff image to the export directory
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    diff_image_filename = f"diff_{timestamp}.png"
    diff_image_path = os.path.join(export_dir, diff_image_filename)
    if not cv2.imwrite(diff_image_path, diff_image):
        logger.error('Failed to write diff image to disk.')
        sys.exit(1)
    logger.info('Diff image saved to %s', diff_image_path)

    # Store the comparison result in the database
    try:
        db_config = config.get('database', {})
        db_path = db_config.get('path', 'results.db')
        conn = init_db(db_path)
        record = {
            'timestamp': timestamp,
            'image1_path': os.path.abspath(args.image1),
            'image2_path': os.path.abspath(args.image2),
            'diff_image_path': os.path.abspath(diff_image_path),
            'differences': str(differences),
            'width': metadata['width'],
            'height': metadata['height'],
            'parameters': f"tolerance={tolerance}"
        }
        insert_comparison_record(conn, record)
        conn.close()
        logger.info('Comparison record inserted into database.')
    except Exception as e:
        logger.exception('Failed to insert record into database: %s', e)
        sys.exit(1)


if __name__ == '__main__':
    main()
