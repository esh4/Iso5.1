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
        grip.process(frame)
        
        lineDetection.displayContours(grip.filter_contours_output)       
        ser.write()
        
    
    else:
        print 'no frame!', i
        time.sleep(1)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    i += 1
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

