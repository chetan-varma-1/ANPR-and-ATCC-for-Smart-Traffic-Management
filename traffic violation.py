#taffic monitoring and license plate detection
# 1. process the video of traffic
# 2. detect traffic light whether its red, yellow , green 
# 3. lane marking(white marks) to track vehicle movement
# 4. vehicle license plate is detected using the haar cascade detection 
# 5. OCR -> Extracting the character from the license plate
# 6. logs violation -> mysql database
# 7. Display the processed video with annotations

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import dbconnection

