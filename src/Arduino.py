class Arduino:
    ser = None
    baud = 4000000
    def __init__(self, baud=self.baud):
        self.baud = baud
    
    def connectArduino(baud):
        arduino_ports = []
        if system == 'Windows':
            arduino_ports.append(raw_input('arduino COM: '))
            
        elif system == 'Linux':
            arduino_ports = [
                    p[0]
                    for p in self.serial.tools.list_ports.comports()
                    if '2341' in p[2]
                    ]
            if not arduino_ports:
                print"No Arduino found"
                #self.ser = None
                return 0
        if len(arduino_ports) > 0:
            self.ser = self.serial.self.serial(arduino_ports[0], 4000000)
            print 'arduino connected!'
        else:
            self.ser = None
            
    def write(self, val1, val2=None):
        if self.ser!=None: 
            val = '<'+str(val1)+'x'+str(val2)+'>'      
            self.ser.write(val)  