from roboflow import Roboflow
import supervision as sv
import cv2

rf = Roboflow(api_key="5ZEncW0XOKAHcjrf2mhO")
project = rf.workspace().project("playing-cards-ow27d")
model = project.version(4).model

"""
result = model.predict("test2.jpg", confidence=50, overlap=50).json()

labels = [item["class"] for item in result["predictions"]]

detections = sv.Detections.from_inference(result)

label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoxAnnotator()

image = cv2.imread("test2.jpg")

annotated_image = box_annotator.annotate(
    scene=image, detections=detections)
annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections, labels=labels)

sv.plot_image(image=annotated_image, size=(16, 16))
"""

def main(cam: cv2.VideoCapture):
    while True:
        getting_frames, image = cam.read()
        if not getting_frames:
            print("No frames received")

        cv2.imwrite( "temp/test.jpg", image)
        result = model.predict("temp/test.jpg", confidence=50, overlap=50).json()
        print(result)

        #cv2.imshow("Predictions", concatenated_image)
        #if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit visualization
            #return

if __name__ == '__main__':
    cam = cv2.VideoCapture(0)
    try:
        main(cam)
    finally:
        cv2.destroyAllWindows()
