import cv2
import base64
import requests
import json

# Roboflow API key and model details
api_key = "5ZEncW0XOKAHcjrf2mhO"
model_endpoint = "playing-cards-ow27d"
version_number = "4"

# Construct the inference URL
url = f"https://detect.roboflow.com/{model_endpoint}/{version_number}?api_key={api_key}"

# Set confidence and overlap thresholds
confidence_threshold = 50
overlap_threshold = 50


def process_frame(frame):
    """
    Process a single frame for inference.
    """
    # Encode frame to JPEG
    success, buffer = cv2.imencode('.jpg', frame)
    if not success:
        print("Failed to encode frame as JPEG.")
        return None

    # Convert to base64 for API
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    # Prepare payload
    payload = {
        "image": f"data:image/jpeg;base64,{img_base64}",  # Include MIME type prefix
        "confidence": confidence_threshold,
        "overlap": overlap_threshold,
    }

    # Send POST request to model endpoint
    response = requests.post(url, json=payload)

    try:
        # Parse response JSON
        result = response.json()
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None

    return result


def display_results(frame, results):
    """
    Draw results (e.g., bounding boxes) on the frame.
    """
    if results and "predictions" in results:
        for prediction in results["predictions"]:
            x, y, w, h = (
                int(prediction["x"] - prediction["width"] / 2),
                int(prediction["y"] - prediction["height"] / 2),
                int(prediction["width"]),
                int(prediction["height"]),
            )
            label = prediction["class"]
            confidence = prediction["confidence"]

            # Draw bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame


# Open video capture
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if no frame is captured

    # Process frame for inference
    result = process_frame(frame)

    # Print inference result (optional)
    print(json.dumps(result, indent=4) if result else "No result")

    # Display processed results on the frame
    #frame_with_results = display_results(frame, result)

    # Show the frame
    #cv2.imshow("Playing Card Detection", frame_with_results)

    # Break on 'q' key press
    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

# Release resources
cap.release()
cv2.destroyAllWindows()


