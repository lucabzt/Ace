import cv2

cam = cv2.VideoCapture(0)

while True:
    rec, frame = cam.read()
    if not rec:
        break
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit visualization
        break