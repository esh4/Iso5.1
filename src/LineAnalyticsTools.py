import cv2
import numpy as np

class LineAnalysis:
    
    debugMode = False
    displayFrames = []
    displayFramesID = []
    displayPlots = []
    displayPlotsID = []
    
        
    def __init__(self, debugMode=False):
        self.debugMode = debugMode
        self.scanLine = 100
        self.grayThresh = 255
        
    def addDisplay(self, pORf, key, img):
        if pORf == 'p':
            self.displayPlotsID.apped(key)
            self.displayPlots.append(img)
        elif pORf == 'f':
            self.displayFramesID.append(key)
            self.displayFrames.append(img)
        else:
            pass
        
    def getDisplay(self):
        return self.displayFramesID,self.displayFrames,self.displayPlotsID,self.displayPlots
        
    def edgeDetect(self, frame):
        src = frame

        kernel = np.array([[-1.0, -1.0, -1.0, -1.0, -1.0],
                           [-1.0, 0, 0, 0, -1.0],
                           [-1.0, 0, 16, 0, -1.0],
                           [-1.0, 0, 0, 0, -1.0],
                           [-1.0, -1.0, -1.0, -1.0, -1.0]]) / 25
        dst = cv2.filter2D(src, -1, kernel)
        
        if self.debugMode:
            cv2.line(dst.copy(), (0, self.scanLine), (640, self.scanLine), (255, 0, 0), 1)
            self.addDisplay('f', 'edge filtered', cv2.line(dst.copy(), (0, self.scanLine), (640, self.scanLine), (255, 0, 0), 1))
            #cv2.imwrite('..\edged.jpg', cv2.cvtColor(dst.copy(), cv2.COLOR_GRAY2BGR))
            self.addDisplay('f', 'gray image', src) 
            
            
        return dst
         
    def getErrorCOG(self, edgedFrame):
        pass
            
    def getErrorHorizontalScan(self, frame):  # find black main across a single horizon
        line2scan = frame[self.scanLine]
        #self.plot(line2scan)
        # print 'frame', frame
        for p in range(len(line2scan)):
            #print line2scan[p]
            if line2scan[p] < 40.0:
                #edge = line2scan[p] 
                #print 'edge:    ', p
                return p        
    
        if self.debugMode:
            self.addDisplay('f', 'followLine input', frame)

    def getContourFrame(self, cnts):
        blackMat = np.zeros((480, 640, 3), np.uint8)
        #print len(cnts)  
        return cv2.drawContours(blackMat, cnts, -1, (0, 255, 0), 3)
        
    def getContourCentroid(self, cont):
        Mc = cv2.moments(cont)
        
        cx = int(Mc['m10']/Mc['m00'])
        cy = int(Mc['m01']/Mc['m00'])
        
        return cx

    def getPlot(self, dataArray):
        # background image for the plot
        blackMat = np.zeros((512, 640, 3), np.uint8)
        
        i = 0  # used for index of array
        for data in dataArray:
            cv2.line(blackMat, (i, 256), (i, data), (255, 0, 0), 1)
            i = i + 1
        return blackMat

class Display:
    frames = []
    frameId = []
    plots = []
    plotId = []
    
    def addFrame(self, key, frame):
        self.frameId.append(key)
        self.frames.append(frame)
        
    def addPlot(self, key, plot):
        self.plotId.append(key)
        self.plots.append(plot)
        
    def addFramesPlots(self, fID, f, pID, p):
        self.frameId.extend(fID)
        self.frames.extend(f)
        self.plotId.extend(pID)
        self.plots.extend(p)
        
    def displayImages(self, system):
        #print system
        if system == 'Windows':
            for k in range(len(self.frames)):
                cv2.imshow(self.frameId[k], self.frames[k])
            
            for k in range(len(self.plots)):
                cv2.imshow(self.plotId[k], self.plots[k])
                
        else:
            pass
        
    def reset(self):
        self.frames = []
        self.frameId = []
        self.plots = []
        self.plotId = []