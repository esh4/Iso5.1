import cv2
import numpy as np

class LineDetection:
    
    debugMode = False
    displayFrames = {}
    displayPlots = {}
    
    def __init__(self, debugMode=False):
        self.debugMode = debugMode
        self.scanLine = 100
        self.grayThresh = 255
    
    def processFrame(self, frame):
        # Our operations on the frame come here
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        filtGrayFrame = cv2.inRange(grayFrame, 0, self.grayThresh)
        
        return self.followLine(self.edgeDetect(filtGrayFrame))
        
        if self.debugMode:
            # cv2.imshow('threshed', grayFrame)
            pass
        
        
        
    def edgeDetect(self, frame):
        src = frame
        '''
        kernel = np.array([[-1.0,-1.0,-1.0],
                           [-1.0,8.0,-1.0],
                           [-1.0,-1.0,-1.0]])/25
                           '''
        kernel = np.array([[-1.0, -1.0, -1.0, -1.0, -1.0],
                           [-1.0, 0, 0, 0, -1.0],
                           [-1.0, 0, 16, 0, -1.0],
                           [-1.0, 0, 0, 0, -1.0],
                           [-1.0, -1.0, -1.0, -1.0, -1.0]]) / 25
        dst = cv2.filter2D(src, -1, kernel)
        
        if self.debugMode:
            cv2.line(dst.copy(), (0, self.scanLine), (640, self.scanLine), (255, 0, 0), 1)
            cv2.imshow('edge filtered', cv2.line(dst.copy(), (0, self.scanLine), (640, self.scanLine), (255, 0, 0), 1))
            cv2.imwrite('..\edged.jpg', cv2.cvtColor(dst.copy(), cv2.COLOR_GRAY2BGR))
            cv2.imshow('gray image', src) 
            
            
        return dst
         
    def findLineCOG(self, edgedFrame):
        sumX, sumY, avgX, avgY = 0, 0, 0, 0
        
        y = 0
        while y < len(edgedFrame):
            x = 0
            while x < len(edgedFrame[y]):
                if edgedFrame[y][x] == 0:
                    pass
                else:
                    sumX = sumX + x
                    sumY = sumY + y
                x = x + 1
            y = y + 1
        avgX = sumX / len(edgedFrame[0])
        avgY = sumY / len(edgedFrame)
            
        edgedFrame = cv2.rectangle(edgedFrame, (avgY - 30, avgX - 30), (avgY + 30, avgX + 30), (255, 0, 0), -1)    
        if self.debugMode:
            cv2.imshow('COG', edgedFrame)
            
    def followLine(self, frame):  # find black line across a single horizon
        line2scan = frame[self.scanLine]
        self.plot(line2scan)
        # print 'frame', frame
        edge = 0
        for p in range(len(line2scan)):
            if line2scan[p] > 100:
                edge = line2scan[p] 
                print 'found edge at', p, 'pixels'
                break
                
        return edge
        if self.debugMode:
            cv2.imshow('followLine input', frame)
            
    def filterContours(self, frame):
        # gets edged image
        _, conts, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        try:
            largeC = conts[0]
            Cx, Cy, Cw, Ch = cv2.boundingRect(largeC)
        except:
            largeC = []
        if self.debugMode:
            cv2.imshow('contour filtered', cv2.drawContours(frame, largeC, -1, (0, 255, 0)))
        

    def plot(self, dataArray):
        # background image for the plot
        blackMat = np.zeros((512, 640, 3), np.uint8)
        
        i = 0  # used for index of array
        for data in dataArray:
            cv2.line(blackMat, (i, 256), (i, data), (255, 0, 0), 1)
            i = i + 1
        if self.debugMode:
            cv2.imshow('plot', blackMat)
            return blackMat

