import numpy as np
import cv2
from LineAnalyticsTools import Display
from LineAnalyticsTools import LineAnalysis
import sys
import os
import time
import serial
import serial.tools.list_ports
import platform
from grip import GripPipeline
from LineFollower import lineFollow
from Arduino import Arduino

line = LineAnalysis(False)
grip = GripPipeline()
system = platform.system()
arduino = Arduino()
print system
#display = Display()
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
    
connectCam()
LF = lineFollow(cap, system, arduino)
try:
    LF.followByTime(1000000000)




except Exception,e:
    print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
    try:
        if 'Errno 5' in str(e) and system != 'Windows':
            print 'arduino reconnect'
            connectArduino()
        if 'No such device' in str(e):
            print 'cam reconnect'
            connectCam()
        if 'picture' in str(e):
            connectCam()
        else:
            pass
        
    except:
        pass
    
        #cap.reconnect()
    
#if cv2.waitKey(1) and 0xFF == ord('q') and system == 'Windows':
#    break
    
    #i += 1
    #except Exception,e:
       # print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e), e)
       
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

