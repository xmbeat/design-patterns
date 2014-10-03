import threading
from pipe_connectors import PipedInputStream, PipedOutputStream
from time import sleep

                
class EndOfStreamException(Exception):
    def __init__(self, message = None):
        Exception.__init__(self)
        self.message = message

class FilterFramework(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__readPort = PipedInputStream()
        self.__writePort = PipedOutputStream()
        
    def connect(self, filter_framework):
        try:
            # Connect this filter's input to the upstream pipe's output stream
            self.__inputFilter = filter_framework
            
            self.__readPort.connect(filter_framework.__writePort)
        except BaseException, error:
            print "{0} FilterFramework error connecting::{1}".format(self.getName(), error)
                      
    def readByte(self):
        try:
            while self.__readPort.available() == 0:
                if self.endOfInputStream():
                    raise EndOfStreamException("End of input stream reached")
                sleep(0.250)
        except EndOfStreamException, error:
            raise error
        except Exception, error:
            print "{0} Error in read port wait loop::{1}".format(self.getName(), error)
        try:
            data = self.__readPort.read()
            return data
        except Exception, error:
            print "{0} Pipe read error::{1}", self.getName(), error
            return 0
    
    def writeByte(self, data):
        try:
            self.__writePort.write(data)
            self.__writePort.flush()
        except Exception, error:
            print "{0} Pipe write error::{1}".format(self.getName(), error)
            
    def endOfInputStream(self):
        return not self.__inputFilter.isAlive()
    
    def closePorts(self):
        try:
            self.__readPort.close()
            self.__writePort.close()
        except Exception, error:
            print "{0} closePorts error::{1}".format(self.getName(), error)
                

            


    