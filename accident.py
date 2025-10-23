import cv2
import time
import numpy as np
from pathlib import Path
from ultralytics import YOLO


class AccidentDetection:
    def __init__(self,model_path,conf_threshold=0.4,enable_gui = True):
        """Intialize the accident detection system."""
        self.conf_threshold=conf_threshold
        self.model_path = model_path
        self.enable_gui = enable_gui
        self.output_dir = Path("accident detection")
        self.output_dir.mkdir(exist_ok=True) 

