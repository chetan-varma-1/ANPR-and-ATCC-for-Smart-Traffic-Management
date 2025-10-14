import cv2
import numpy as np 
from ultralytics import YOLO # YOLO(YOLO ONLY LOOK ONCE - OBJECT  DETECTION  YOLOV8-BETTER ACURRACY AND SPEED)
import os

#function to simulate a traffic light on the frame at a responsive position

def simulate_traffic_light(frame, light_state, position):
    """simulates a traffic light at the given position on the frame.
       args:
       frame: the value fram to draw the traffic light on.
       light_state:current state of the light(0-red, 1-yellow, 2-green)
       position:(x,y) coordinates of the top left corner of the traffic light"""
    traffic_light_colors = [(0,0,255),(0,255,255),(0,255,0)]#bgr
    x,y = position
    #draw the traffic light housing
    cv2.rectangle(frame,(x,y),(x+50,y+150),(50,50,50),-1)
    #draw the light
    for i,color in enumerate(traffic_light_colors):
        cv2.circle(frame,(x + 25,y + 25 + i*50), 15, color if i == light_state else (50,50,50),-1)


#function to determine signal color based on vehicle count
def determine_signal(total_vehicles):
    """Determine the signal color and corresponing traffic light state based on vehicle count
    Args:
    total_vehicles :total numbers of detected vehicles
    return:
     tuples of signal color name, BGR color, and light state index."""
    if total_vehicles < 10:
        return "Green", (0,255,0), 2
    elif total_vehicles < 20:
        return "Yellow", (0,255,255), 1
    else:
        return "Red", (0,0,255), 0 

#function to load videos from a folder
def load_video_from_folder(video_folder):
    """Load all video files from the provided folder"""
    video_files=[] #{"path": "C:\Users\cheta\Desktop\Automatic Number Plate Recognition (ANPR) _ Vehicle Number Plate Recognition (1).mp4","road_name":"Automatic Number Plate Recognition (ANPR) _ Vehicle Number Plate Recognition (1).mp4"}
    for filename in os.listdir(video_folder):
        if filename.endswidth(".mp4"):
            video_files.append({"path":os.path.join(video_folder, filename),"road_name":filename})
    return video_files

#function to process individual frames
def process_frame(frame,model,road_name,directions):#{left:2,right:3}
    '''
    process a video frame: Detect objects,classify direction, and overlay information.
    Args:
    Frame: The input video frame.
    model: The YOLO Model for object detection
    road_name: name of the file .
    directions: Dictionary to count vehicle directions.

    Returns: Processed frame with detection overlays and vehicle count per direction.
    '''
    results = model(frame)
    detections = results[0].boxes.data.cpu().numpy() #{x1,y1,x2,y2, confidence(0-1), class_id #0-bikes,1-cars,2-trucks}
    vehicle_count= {"car":0,"truck":0,"motorcycle":0,"bus":0}
    
    for det in detections:
        x1, y1, x2, y2, conf , class_id = det
        class_id =int(class_id)
        label = model.names[class_id]  #  ["car","truck","motorcycle","bus"]
        if label in vehicle_count:
            vehicle_count[label]+=1
            center_x = (x1+x2)/2
            if center_x < frame.shape[1]/2:
                directions["left"] += 1
            else:
                directions["right"]+= 1
            
            color = (0,255,0) if conf > 0.5 else (0,0,255) #bgr
            cv2.rectangle(frame,(int(x1),int(y1)),(int(x2),int(y2)),color,2) 
            cv2.putText(frame,f"{label}{conf:.2f}",(int(x1),int(y1)-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)

            # Add file name and vehicle information to the frame
            cv2.putText(frame,f"File :{road_name}",(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            y_offf



