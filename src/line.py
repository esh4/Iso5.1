import numpy as np
import cv2
from LineDetection import LineDetection

cap = cv2.VideoCapture(0)
measureLine = 100
lineDetection = LineDetection(True)

def dud(num):
    pass

cv2.namedWindow('control')
cv2.createTrackbar('horizon', 'control', 255, 255, dud)

i = 0
while(i<1):
    #Capture frame-by-frame
    ret, frame = cap.read()
    #for custom frame analysis
    frame = cv2.imread('../test.png')
    #pretty important
    frame = cv2.resize(frame, (640, 480))
    
    #gray image thersh holding
    lineDetection.grayThresh = 43#cv2.getTrackbarPos('horizon', 'control')
    
    #main function to find line
    lineDetection.processFrame(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i +=0
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

