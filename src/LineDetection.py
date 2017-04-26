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
         
    def getErrorCOG(self, edgedFrame):
        sumX, sumY, avgX, avgY = 0, 0, 0, 0
        
        y = 0
        while y < len(edgedFrame):
            x = 0
            while x < len(edgedFrame[y]):
                if edgedFrame[y][x] == 0:
                    print 'continue COG'
                    continue
                sumX = sumX + x
                sumY = sumY + y
                x += 1
                print 'x:', x
            y += 1
            print 'y:',y
        avgX = sumX / len(edgedFrame[0])
        avgY = sumY / len(edgedFrame)
        
        print 'avgX: ', avgX, 'avgY: ', avgY
        edgedFrame = cv2.rectangle(edgedFrame, (avgY - 30, avgX - 30), (avgY + 30, avgX + 30), (255, 0, 0), -1)    
        if self.debugMode:
            cv2.imshow('COG', edgedFrame)
            
    def getErrorHorizontalScan(self, frame):  # find black main across a single horizon
        line2scan = frame[self.scanLine]
        self.plot(line2scan)
        # print 'frame', frame
        edge = 0
        first_byte=second_byte=0
        for p in range(len(line2scan)):
            if line2scan[p] > 50:
                edge = line2scan[p] 
                #print 'found edge at', p, 'pixels'
                #changed the printing to 'edge',not 'p'
                print 'found edge at', p, 'pixels. value is:',edge
                #take the first two bytes
                first_byte = p & 0x000000FF
                second_byte = p & 0x0000FF00
                second_byte = second_byte>>8
                print 'bytes:',second_byte,'|',first_byte
                break
        #else:
         #   print 'no main'
                
        #changed to return two bytes representing p
        return [first_byte,second_byte]
        if self.debugMode:
            cv2.imshow('followLine input', frame)

    def displayCountours(self, cnts):
        blackMat = np.zeros((480, 640, 3), np.uint8)
        cv2.drawContours(blackMat, cnts, -1, (0, 255, 0), 3)  
        

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

