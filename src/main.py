import numpy as np
import cv2
from LineAnalyticsTools import Display
from LineAnalyticsTools import LineAnalysis
import sys
#from Communication import ArduinoCom
import time
import serial
import platform
from grip import GripPipeline
from ipCamera import ipCamera

ret, cap = True, ipCamera('http://raspberrypi.local:8081')
line = LineAnalysis(False)
grip = GripPipeline()
system = platform.system()
display = Display()


try:
    if system == 'Linux':
        ser = serial.Serial('/dev/ttyUSB0', 9600)
    elif system == 'Windows':
        ser = serial.Serial(raw_input('input arduino COM port'), 9600)
except Exception,e:
    ser = None
    print 'serial connection err', str(e)

def dud(num):
    pass

i = 1

while(i>0):
    display.reset()
    #Capture frame-by-frame
    #ret, frame = cap.read()
    
    #frame = cv2.imread('test.png')
    frame = cap.getFrame()
    if ret:
        grip.process(frame)
                
        display.addFrame('filtered contours', line.getContourFrame(grip.filter_contours_output))
        
        print 'centroid', line.getContourCentroid(grip.filter_contours_output[0])
        
        
        
        display.addFrame('cvt', grip.cv_cvtcolor_output)
        display.addFrame('thresh',grip.cv_threshold_output)
        
        if ser!=None:       
            ser.write()
            
        display.addFramesPlots(line.displayFramesID,line.displayFrames,line.displayPlotsID,line.displayPlots)
        display.displayImages(system)
    
    else:
        print 'no frame!', i
        time.sleep(1)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    i += 1
    #except Exception,e:
       # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
       
# When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()

