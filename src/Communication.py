import smbus
import time

class ArduinoCom:
    bus = 0
    address = 0x0
    
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x04
        
    def writeData(self, value):
        #value is an array of size 2
        try:
            self.bus.write_byte_data(self.address, 0x00, value[0])
            self.bus.write_byte_data(self.address, 0x00, value[1])
            
            #self.bus.write_byte_data(self.address, 0x00, value)
        except Exception,e:
            print str(e)
        
    def readData(self):
        try:
            return self.bus.read_byte_data(self.address, 0)
        except Exception,e:
            print str(e)