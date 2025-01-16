import cv2
import numpy as np
import os


def colorDetection(image):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    '''Red'''
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

    '''Yellow'''
    # Range for yellow
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Combine masks for red and yellow
    combined_mask = mask_red + mask_yellow

    # Apply the mask to the image
    result = cv2.bitwise_and(image, image, mask=combined_mask)

    # Calculate the percentage of red and yellow in the image
    red_ratio = (cv2.countNonZero(mask_red)) / (image.size / 3) * 100
    yellow_ratio = (cv2.countNonZero(mask_yellow)) / (image.size / 3) * 100

    print("Red in image:", np.round(red_ratio, 2), "%")
    print("Yellow in image:", np.round(yellow_ratio, 2), "%")

    return result


# Load and test every image in a folder
def load_and_test_images_in_folder(folder_path):
    # Get all files in the folder
    for filename in os.listdir(folder_path):
        # Build the full file path
        file_path = os.path.join(folder_path, filename)

        # Check if the file is an image (common formats)
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            # Load the image
            image = cv2.imread(file_path)

            if image is None:
                print(f"Error: Could not load image at {file_path}")
                continue

            print(f"Processing image: {filename}")

            # Call the color detection function
            result = colorDetection(image)

            # Display the original and processed (result) image
            cv2.imshow("Original Image", image)
            cv2.imshow("Red and Yellow Detected", result)

            # Wait for any key press to move to the next image
            cv2.waitKey(0)

    # Clean up OpenCV windows once done
    cv2.destroyAllWindows()


# Specify the folder containing the test images
test_folder_path = "images"  # Replace this with your folder path

# Execute
load_and_test_images_in_folder(test_folder_path)
