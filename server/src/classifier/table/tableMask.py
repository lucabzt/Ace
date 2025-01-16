import cv2
import numpy as np
import os


def refine_bounding_box(image, coordinates, padding=0.05):
    """
    Refine the bounding box using provided coordinates of the spades or target regions.
    :param image: Original image.
    :param coordinates: List of coordinates (x, y, w, h) for detected objects (spades, etc.).
    :param padding: Padding percentage to add around the bounding box.
    :return: Refined bounding box (x_min, y_min, x_max, y_max).
    """
    if len(coordinates) == 0:
        return 0, 0, image.shape[1], image.shape[0]  # If no objects, return the full image

    # Initialize bounds
    x_min, y_min, x_max, y_max = image.shape[1], image.shape[0], 0, 0

    # Calculate the bounding box around all provided coordinates
    for x, y, w, h in coordinates:
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
    Detect the coordinates of the two red spades and yellow rectangles with yellow outlines.
    :param image: Input image.
    :return: Detected coordinates, visualization mask.
    #TODO PLAY AROUND HERE !!!!!!!
    #TODO PLAY AROUND HERE !!!!!!!
    #TODO PLAY AROUND HERE !!!!!!!
    #TODO PLAY AROUND HERE !!!!!!!
    """
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Detect red regions (spades)
    red_lower1 = np.array([0, 120, 70])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([170, 120, 70])
    red_upper2 = np.array([180, 255, 255])
    mask_red = cv2.inRange(hsv, red_lower1, red_upper1) + cv2.inRange(hsv, red_lower2, red_upper2)

    # Detect yellow regions (rectangles' outlines)
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Perform edge detection (Canny) to detect outlines
    edges_yellow = cv2.Canny(mask_yellow, 100, 200) #TODO PLAY AROUND HERE !!!!!!!

    # Find contours for both red spades and yellow outlines
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_yellow, _ = cv2.findContours(edges_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    spades = []
    rectangles = []

    # Process red contours (spades)
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        # Get the region of interest (ROI) to check the mean color
        roi = image[y:y + h, x:x + w]
        mean_color = np.mean(roi, axis=(0, 1))  # Calculate mean color for the region (in BGR)

        # Detect spades (red)
        if 0.5 < aspect_ratio < 2 and w > 20 and h > 20:  #TODO PLAY AROUND HERE !!!!!!!
            if is_color_in_range(mean_color, red_lower1, red_upper1) or is_color_in_range(mean_color, red_lower2, red_upper2):
                spades.append((x, y, w, h))

    # Process yellow contours (rectangles with yellow outline)
    for contour in contours_yellow:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        # Rectangles should be large and rectangular in shape
        if w > 60 and h > 60 and h < 200 and w < 200: #TODO PLAY AROUND HERE !!!!!!!
            rectangles.append((x, y, w, h))

    # Create a visualization of the mask
    mask_visualization = np.zeros_like(image)
    mask_visualization[:, :, 2] = mask_red  # Red areas highlighted in red
    mask_visualization[:, :, 1] = mask_yellow  # Yellow areas highlighted in green

    return spades, rectangles, mask_visualization


def is_color_in_range(mean_color, lower_range, upper_range):
    """
    Check if the mean color is within the specified HSV color range.
    :param mean_color: The mean color to check (BGR format).
    :param lower_range: The lower bound of the color range (HSV format).
    :param upper_range: The upper bound of the color range (HSV format).
    :return: True if the mean color is within the range, otherwise False.
    """
    # Convert BGR color to HSV
    mean_color_hsv = cv2.cvtColor(np.uint8([[mean_color]]), cv2.COLOR_BGR2HSV)[0][0]

    # Check if the color is in range
    return cv2.inRange(np.uint8([[mean_color_hsv]]), lower_range, upper_range)[0][0] > 0


def crop_and_transform(image, spades, padding=0.05):
    """
    Crop and transform the image to focus on the area of interest with the original aspect ratio.
    :param image: Original input image.
    :param spades: Coordinates of detected spades.
    :param padding: Padding percentage around the bounding box.
    :return: Image with highlighted rectangle and cropped image with original aspect ratio.
    """
    if len(spades) < 2:
        print("Error: Could not detect two spades. Returning the full image.")
        return image, image

    # Sort spades by x-coordinate to determine the left and right spades
    spades = sorted(spades, key=lambda x: x[0])
    left_spade = spades[0]
    right_spade = spades[-1]

    # Define the bounding box from the left spade to the right spade
    x_min, y_min, x_max, y_max = refine_bounding_box(image, [left_spade, right_spade], padding)

    # Highlight the selected area in the original image (without resizing)
    highlighted_image = image.copy()
    cv2.rectangle(highlighted_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 3)

    # Crop the image to the bounding box
    cropped_image = image[y_min:y_max, x_min:x_max]

    return highlighted_image, cropped_image


def process_image(image):
    """
    Process the input image to detect, highlight, and crop the desired region.
    :param image: Input image.
    :return: Highlighted original image, cropped image, and mask visualization.
    """
    # Detect regions of interest
    spades, others, mask_visualization = detect_regions(image)

    # Highlight detected spades and rectangles with nametags
    for x, y, w, h in spades:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 3)  # Red border for spades
        cv2.putText(image, "Spade", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)  # Nametag for spades
    for x, y, w, h in others:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 3)  # Yellow border for rectangles
        cv2.putText(image, "Rectangle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255),
                    2)  # Nametag for rectangles

    # Crop and highlight the area of interest
    highlighted_image, cropped_image = crop_and_transform(image, spades)

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
            cv2.imshow("Original Image with Highlighted Objects", highlighted_image)
            cv2.imshow("Cropped and Resized Image", cropped_image)
            cv2.imshow("Color Highlighted Mask (Red and Yellow)", mask_visualization)

            # Wait until a key is pressed
            cv2.waitKey(0)

    # Close all OpenCV windows
    cv2.destroyAllWindows()


# Specify the folder path containing the input images
test_folder_path = "images"  # Change this to your folder path

# Process the images
load_and_test_images_in_folder(test_folder_path)
