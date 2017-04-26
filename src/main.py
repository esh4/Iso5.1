import numpy as np
import cv2
from LineDetection import LineDetection
#sfrom Communication import ArduinoCom
import time
import serial
import platform
from grip import GripPipeline

cap = cv2.VideoCapture(0)
lineDetection = LineDetection(True)
#arduino = ArduinoCom()
grip = GripPipeline()


try:
    ser = serial.Serial('COM5', 9600)
except Exception,e:
    print str(e)

def dud(num):
    pass

if lineDetection.debugMode:
    cv2.namedWindow('control')
    cv2.createTrackbar('filter', 'control', 255, 255, dud)
    cv2.createTrackbar('horizon', 'control', 100, 480, dud)

i = 1

#ser.write('16')
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
        px = lineDetection.getErrorHorizontalScan(edgedFrame)
            
        #if ser.readline() != None:
        ser.write(px)
        #print 'sent!'
    
    else:
        print 'no frame!', i
        time.sleep(1)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i += 1
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

