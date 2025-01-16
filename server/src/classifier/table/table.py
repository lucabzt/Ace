import cv2
import numpy as np
import pytesseract
import os


def refine_bounding_box(image, contours, padding=0.05):
    """
    Calculate the bounding box that includes all contours, with added padding.
    :param image: Original image.
    :param contours: Contours detected from the mask.
    :param padding: Padding percentage to add around the bounding box.
    :return: Refined bounding box (x_min, y_min, x_max, y_max).
    """
    if len(contours) == 0:
        return 0, 0, image.shape[1], image.shape[0]  # If no contours, return the full image

    # Initialize bounds
    x_min, y_min, x_max, y_max = image.shape[1], image.shape[0], 0, 0

    # Find the bounding box around all contours
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)

    # Calculate padding based on image size
    padding_x = int(padding * image.shape[1])
    padding_y = int(padding * image.shape[0])

    # Apply padding and ensure bounds are within image dimensions
    x_min = max(0, x_min - padding_x)
    y_min = max(0, y_min - padding_y)
    x_max = min(image.shape[1], x_max + padding_x)
    y_max = min(image.shape[0], y_max + padding_y)

    return x_min, y_min, x_max, y_max


def detect_regions(image):
    """
    Detect red and yellow regions in the input image.
    :param image: Input image.
    :return: Combined mask of red and yellow regions, contours, and mask visualization image.
    """
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    '''Red Detection'''
    # Range for lower red
    red_lower1 = np.array([0, 120, 70])
    red_upper1 = np.array([10, 255, 255])
    mask_red1 = cv2.inRange(hsv, red_lower1, red_upper1)

    # Range for upper red
    red_lower2 = np.array([170, 120, 70])
    red_upper2 = np.array([180, 255, 255])
    mask_red2 = cv2.inRange(hsv, red_lower2, red_upper2)

    # Combine red masks
    mask_red = mask_red1 + mask_red2

    '''Yellow Detection'''
    # Range for yellow
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([35, 255, 255])
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    '''Combined Mask'''
    # Combine masks for red and yellow
    combined_mask = cv2.bitwise_or(mask_red, mask_yellow)

    # Find the contours from the combined mask
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a visualization of the mask
    mask_visualization = np.zeros_like(image)
    mask_visualization[:, :, 2] = mask_red  # Red areas highlighted in red
    mask_visualization[:, :, 1] = mask_yellow  # Yellow areas highlighted in green

    return combined_mask, contours, mask_visualization


def crop_and_transform(image, contours):
    """
    Crop and transform the image to focus on the area of interest.
    :param image: Original input image.
    :param contours: Detected contours from the mask.
    :return: Highlighted image with bounding box and cropped image.
    """
    # Refine the bounding box around the detected regions
    bounding_box = refine_bounding_box(image, contours)

    # Crop the image to the bounding box
    x_min, y_min, x_max, y_max = bounding_box
    cropped_image = image[y_min:y_max, x_min:x_max]

    # Resize the cropped area for consistent display
    resized_image = cv2.resize(cropped_image, (800, 600), interpolation=cv2.INTER_CUBIC)

    # Create a highlighted version of the original image
    highlighted_image = image.copy()
    cv2.rectangle(highlighted_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)  # Green rectangle

    return highlighted_image, resized_image


def process_image(image):
    """
    Process the input image to detect, highlight, and crop the desired region.
    :param image: Input image.
    :return: Highlighted original image, cropped image, and mask visualization.
    """
    # Detect yellow and red regions
    combined_mask, contours, mask_visualization = detect_regions(image)

    # Crop and transform the image to focus on the detected area
    highlighted_image, cropped_image = crop_and_transform(image, contours)

    return highlighted_image, cropped_image, mask_visualization


def load_and_test_images_in_folder(folder_path):
    """
    Load and process all images in the specified folder.
    :param folder_path: Path containing input images.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Read the image
            image = cv2.imread(file_path)

            if image is None:
                print(f"Error: Could not load image at {file_path}")
                continue

            print(f"Processing image: {filename}")

            # Process the image
            highlighted_image, cropped_image, mask_visualization = process_image(image)

            # Show the results
            cv2.imshow("Original Image with Highlighted Region", highlighted_image)
            cv2.imshow("Cropped and Resized Image", cropped_image)
            cv2.imshow("Color Highlighted Mask (Red and Yellow)", mask_visualization)

            # Wait until a key is pressed
            cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# Specify the folder path that contains input images
test_folder_path = "images"  # Change this to your folder path

# Process the images
load_and_test_images_in_folder(test_folder_path)
