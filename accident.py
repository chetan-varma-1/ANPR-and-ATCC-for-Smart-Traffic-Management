import cv2
import time
import numpy as np
from pathlib import Path
from ultralytics import YOLO


class AccidentDetection:
    def __init__(self,model_path,conf_threshold=0.4,enable_gui = True):
        """Intialize the accident detection system."""
        self.conf_threshold = conf_threshold
        self.enable_gui = enable_gui
        self.output_dir = Path("accident detection")
        self.output_dir.mkdir(exist_ok=True) 

        try:
            # Load Yolov8 model
            self.model = YOLO(model_path)
            print("Model loaded sucessfully")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def process_frame(self,frame):
        """process a single frame and return detections."""
        try:
            #perform detection
            results = self.model(frame,conf=self.conf_threshold)
            return results[0] #return first result
        except Exception as e:
            print(f"Error processing frame:{str(e)}")
            return None
    
    def process_video_with_gui(self, video_path):
        """process multiple video feeds and display them in a grid GUI."""
        caps = [cv2.VideoCapture(path) for path in video_path]
        target_width,target_height = 640,480 #consistent frame size for stacking

        while True:
            frames = []
            for cap in caps:
                rect, frame = cap.read()
                if rect:
                    frame_resized = cv2.resize(frame, (target_width,target_height))
                    results = self.process_frame(frame_resized)

                    #process detections

                    if results is not None:
                        for box in results.boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            conf = box.conf[0].cpu().numpy()
                            if conf > self.conf_threshold:
                                cv2.rectangle(frame_resized,(int(x1),int(y1)),(int(x2),int(y2)),(0,255,0),2)
                                cv2.putText(frame_resized,(int(x1),int(y1)-10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                    
                    frames.append(frame_resized)
                else:
                    frames.append(None)

            #Remove none frames and stack them
            valid_frames = [f for f in frames if f is not None]
            
            print(len(valid_frames))

            #stack frames into a grid #0:2->0,1
            rows =[valid_frames[i:i+2] for i in range(0,len(valid_frames),2)] #0->3->5
            stacked_rows = [np.hstack(row) for row in rows]
            grid_frame = np.vstack(stacked_rows)

            #display the grid
            cv2.imshow("Accident Detection System",grid_frame)
            if cv2.waitKey(1) & 0xFF ==ord('q'):
                break

            #release all resources
            for cap in caps:
                cap.release()
            cv2.destroyAllWindows()
    @staticmethod
    def detect_accident(video_path):
        """static method to intialize and run accident detection"""
        MODEL_PATH = r"C:\Users\cheta\Desktop\ANPR and ATCC for Smart Traffic Management\best.pt"
        CONFIDENCE_THRESHOLD = 0.4

        try:
            detector = AccidentDetection(MODEL_PATH,CONFIDENCE_THRESHOLD,enable_gui=True)
            detector.process_video_with_gui(video_path)
        except Exception as e:
            print(f"Error:{str(e)}")


if __name__ == "__main__":
    AccidentDetection.detect_accident(




            



    

