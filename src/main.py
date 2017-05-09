import numpy as np
import cv2
from LineAnalyticsTools import Display
from LineAnalyticsTools import LineAnalysis
import sys
import os
#from Communication import ArduinoCom
import time
import serial
import serial.tools.list_ports
import platform
from grip import GripPipeline
from ipCamera import ipCamera
#import warnings

line = LineAnalysis(False)
grip = GripPipeline()
system = platform.system()
print system
display = Display()
ser = None

def connectArduino():
    global ser
    arduino_ports = [
            p[0]
            for p in serial.tools.list_ports.comports()
            if '2341' in p[2]
            ]
    if not arduino_ports:
        print"No Arduino found"
        #ser = None
        return 0
    if len(arduino_ports) > 0:
        ser = serial.Serial(arduino_ports[0], 4000000)
    else:
        ser = None

cap = None
def connectCam():
    global cap
    if cap != None:
        cap.release()
    cameraPort = 0
    if system == 'Linux':
        n = os.popen('sudo ls /dev/video*').read()
        c = [int(s) for s in list(n) if s.isdigit()]
        print n, c
        cameraPort = c[0]
    else:
        cameraPort = int(raw_input('enter cam port'))
    cap = cv2.VideoCapture(cameraPort)
    
oldFrame = None
i = 1
connectArduino()
connectCam()

while(i>0):
    display.reset()
    #Capture frame-by-frame
    #ret, frame = cap.read()
    
    #frame = cv2.imread('test.png')
    try:
        ret, frame = cap.read()
        if np.array_equal(frame, oldFrame) and system != 'Windows':
            print 'identical frames'
            connectCam()    
        if ret:#type(frame) == 'numpy.ndarray':
            grip.process(frame)
                    
            display.addFrame('filtered contours', line.getContourFrame(grip.filter_contours_output))
            
            setpoint = line.getContourCentroid(grip.filter_contours_output[0])
            #print 'centroid:    ', setpoint
            
            #edge = line.getErrorHorizontalScan(grip.cv_cvtcolor_output)
            #print 'edge detected:    ', setpoint
            #setpoint = (edge + cog)/2
            
            
            display.addFrame('cvt', grip.cv_cvtcolor_output)
            display.addFrame('thresh',grip.cv_threshold_output)
            
            if ser!=None: 
                val = '<'+str(setpoint)+'>'      
                ser.write(val)
                
            display.addFramesPlots(line.displayFramesID,line.displayFrames,line.displayPlotsID,line.displayPlots)
            display.displayImages(system)
            
            oldFrame = frame
        else:
            print 'no frame!', i
            connectCam()
    except Exception,e:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
        try:
            if 'Errno 5' in str(e) and system != 'Windows':
                print 'arduino reconnect'
                connectArduino()
            if 'No such device' in str(e):
                print 'cam reconnect'
                connectCam()
            else:
                pass
            
        except:
            pass
        
            #cap.reconnect()
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    i += 1
    #except Exception,e:
       # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
       
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

