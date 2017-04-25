import numpy as np
import cv2
from LineDetection import LineDetection
from Communication import ArduinoCom
import time

cap = cv2.VideoCapture(0)
lineDetection = LineDetection(False)
arduino = ArduinoCom()

def dud(num):
    pass

if lineDetection.debugMode:
    cv2.namedWindow('control')
    cv2.createTrackbar('filter', 'control', 255, 255, dud)
    cv2.createTrackbar('horizon', 'control', 100, 480, dud)

i = 1
while(i>0):
    #Capture frame-by-frame
    ret, frame = cap.read()
    #frame = cv2.imread('test.png')
    if ret:
        
        #pretty important
        frame = cv2.resize(frame, (640, 480))
        
        #gray image thersh holding
        if lineDetection.debugMode:
            lineDetection.grayThresh = cv2.getTrackbarPos('filter', 'control')
            lineDetection.scanLine = cv2.getTrackbarPos('horizon', 'control')
        
        else:
            lineDetection.grayThresh = 50
            lineDetection.scanLine = 300
            
        #main function to find line
        edgedFrame = lineDetection.edgeDetect(lineDetection.processFrame(frame))
        px = lineDetection.followLine(edgedFrame)
        
        arduino.writeData(px)
    
    else:
        print 'no frame!', i
        time.sleep(1)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i += 1
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

