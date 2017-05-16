import cv2
from grip import GripPipeline
import time
from LineAnalyticsTools import LineAnalysis
import math

class lineFollow:
    cam = None
    grip = None
    line = None
    frame = None
    oldFrame = None
    system = None
    arduino = None
    
    setpoint = 320
    
    def __init__(self, cam, system, arduino):
        self.cam = cam
        self.grip = GripPipeline()
        self.line = LineAnalysis(False)
        self.system = system
        self.arduino = arduino
    
    def followOneStep(self, side):
        ret, self.frame = self.cam.read()
        if np.array_equal(self.frame, self.oldFrame) and system != 'Windows':
            print 'identical frames'
            connectCam()    
            return None
        if ret:
            roi = line.getRoi(self.frame)
            grip.process(roi)     
            self.setpoint = line.findLineRoi(grip.cv_threshold_output, side)
            self.oldFrame = self.frame
            return self.setpoint
        else:
            raise Exception("no picture mate!")
        
    def followByTime(self, seconds, side=-1):
        timout = time.time() + seconds
        
        while time.time() < timout:
            spdReduce = self.getCurveGain()
            corecction = self.followOneStep(side)
            arduino.write(correction, spdReduce)
            
    def getCurveGain(self):
        topRoi = line.getRoi(self.frame, 0)
        topLineX = line.findLineRoi(topRoi, -1)
        bottonLineX = self.setpoint
        Dx = abs(topLineX - bottonLineX)
        Dy = 480/3*2 - 0 
        curveAngle = math.degrees(math.atan(Dx/Dy))
        return curveAngle
            