import cv2
import base64
import urllib2
import numpy as np
import requests
import time

class ipCamera(object):
    url = ''
    
    def __init__(self, url):
        while(True):
            try:
                self.url = url
                self.stream = requests.get(self.url, stream=True)
                self.bytes = b''
                print('Connected to IP Camera')
                break
            except:
                print 'no cam yet'
                time.sleep(1)
                pass
        
    def getFrame(self):
        #self.bytes = b''
        self.bytes+=self.stream.raw.read(16384)
        a = self.bytes.find(b'\xff\xd8')
        b = self.bytes.find(b'\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),
                                 cv2.IMREAD_COLOR)
            return frame
        
    
    def reconnect(self):
        try:
            print 'trying to connect'
            self.stream = requests.get(self.url, stream=True)
        except:
            print 'cant connect'