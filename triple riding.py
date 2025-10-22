import cv2
from ultralytics import YOLO


#load yolov8 model 
model = YOLO('yolov8s.pt') # yolov8s is the smaller version

#set classes for motorbike and person
motorbike_class = 3  # class ID for "motorbike" in coco dataset
person_class = 0  # class ID for "person" in coco dataset
def detect_triple_riding(video_path):
    # open video file or capture device
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: unable to open video.")
        return 
    
    while True:
        rect,frame = cap.read()
        if not rect:
            break

        # perform object detection
        results = model(frame)


        #