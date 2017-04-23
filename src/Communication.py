import smbus
import time

class ArduinoCom:
    bus = 0
    address = 0x0
    
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x04
        
    def writeData(self, value):
        try:
            self.bus.write_byte(value)
        except:
            print 'you idiot!'
        
    def readData(self):
        try:
            return self.bus.read_byte(self.address)
        except:
            print 'you idiot!'