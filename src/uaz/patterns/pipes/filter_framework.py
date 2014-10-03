import threading
from time import sleep


class PipedOutputStream:
    def __init__(self):
        self.__sink = None
        self._cond = threading.Condition()
    
    def connect(self, sink):
        self._cond.acquire()
        if sink is None:
            self._cond.release()
            raise Exception("Null pointer exception")
        elif (self.__sink is not None or sink._connected):
            self._cond.release()
            raise Exception("Already connected")            
        self.__sink = sink
        sink.__in = -1
        sink.__out = 0
        sink._connected = True
        self._cond.release()
    
    def write(self, data):
        if (self.__sink is None):
            raise Exception("Pipe not connected")
        self.__sink._receive_(data)
        
    def flush(self):
        sink = self.__sink
        if sink is not None:
            sink._cond.acquire()
            sink._cond.notifyAll()
            sink._cond.release()
    
    def close(self):
        sink = self.__sink
        if sink is not None:
            sink._received_last_()
            
class PipedInputStream:
    def __init__(self):
        self.__buffer = bytearray(1024)
        self._cond = threading.Condition()
        self.__in = -1
        self.__out = 0
        self.__close_by_reader = False #Volatile
        self.__close_by_writer = False
        self.__read_side = None
        self.__write_side = None
        self._connected = False
    def connect(self, src):
        src.connect(self)
    
    def close(self):
        self.__close_by_reader = True
        self._cond.acquire()
        self.__in = -1
        self._cond.release()
        
    def read(self):
        if not self._connected:
            raise Exception("Pipe not connected")
        elif self.__close_by_reader:
            raise Exception("Pipe closed")
        elif self.__write_side is not None and not self.__write_side.isAlive() and not self.__close_by_reader and self.__in < 0:
            raise Exception("Write end dead")
        self.__read_side = threading.current_thread()
        trials = 2;
        while self.__in < 0 :
            if self.__close_by_writer:
                #closed by writer, return EOF
                return -1
            if (self.__write_side is not None and self.__write_side.isAlive()):
                trials -= 1
                if trials < 0:
                    raise Exception("Pipe broken")            
            #might be a writer waiting
            self._cond.notifyAll()
            self._cond.wait(1000)
        
        ret = self.__buffer[self.__out]
        self.__out += 1
        
        if (self.__out >= len(self.__buffer)):
            self.__out = 0;

        if (self.__in == self.__out):
            # now empty 
            self.__in = -1;

        return ret;
       
    def available(self):
        self._cond.acquire()      
        if self.__in < 0:
            aux = 0
        elif self.__in == self.__out:
            aux =  len(self.__buffer)
        elif self.__in > self.__out:
            aux = self.__in - self.__out;
        else:
            aux = self.__in + len(self.__buffer) - self.__out;
        self._cond.release()
        return aux
    
    def __check_state__(self):
        if self._connected == False:
            raise Exception("Pipe not connected")
        elif self.__close_by_reader or self.__close_by_writer:
            raise Exception("Pipe closed")
        elif (self.__read_side is not None) and (not self.__read_side.isAlive()):
            raise Exception("Read end dead")
        
    def _await_space_(self):
        while self.__in == self.__out:
            self.__check_state__()
            # full: kick any waiting readers
            self._cond.notifyAll()
            self._cond.wait(1000)
    
    def _receive_(self, b):
        self._cond.acquire()
        self.__check_state__()
        self.__write_side = threading.current_thread()
        
        if (self.__in == self.__out):
            self._await_space_()
            
        if (self.__in < self.__out):
            self.__in = 0
            self.__out = 0
        
        self.__buffer[self.__in] = b
        self.__in += 1
        
        if (self.__in >= len(self.__buffer)):
            self.__in = 0
    
    def _received_last_(self):
        self._cond.acquire()
        self.__close_by_writer = True
        self._cond.notify_all()
        self._cond.release()
    
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
                
class EndOfStreamException(Exception):
    def __init__(self, message = None):
        Exception.__init__(self)
        self.message = message


class MiddleFilter(FilterFramework):
    
    def run(self):
        read = 0        #Cantidad de bytes leidos
        written = 0     #Cantidad de bytes escritos
        data = 0        #El byte leido de la entrada

        #A continuacion un mensaje a la terminal para avisar al mundo que estamos vivo...
        print "{0}::Middle Reading ".format(self.getName())

        while (True):
            ##########################################################
            #    Aqui leemos un byte y escribimos un byte
            ##########################################################
            try:
                data = self.readByte()
                read += 1
                self.writeByte(data)
                written += 1
            except EndOfStreamException:
                self.closePorts()
                print "{0}::Middle Exiting; bytes read: {1}, bytes written{2}".format(self.getName(), read, written)
                break
            
class SinkFilter(FilterFramework):
    def __init__(self):
        FilterFramework.__init__(self)
    def run(self):
        print "{0}::Sink reading".format(self.getName())
        bytesRead = 0
        while True:
            try:
                data = self.readByte()
                bytesRead += 1
                print str(data)               
            except:
                self.closePorts()
                print "{0}::Sink Exiting; bytes read: {1}".format(self.getName(), bytesRead)
                break
class SourceFilter(FilterFramework):
    def __init__(self, filename):
        FilterFramework.__init__(self)
        self.__filename = filename
    def run(self):
        try:            
            fileInput = open(self.__filename, 'r')
            bytesRead = 0
            bytesWritten = 0
            print "{0}::Source reading file..".format(self.getName())
            while (True):
                data = fileInput.read(1)
                if data:
                    bytesRead += 1
                    self.writeByte(data)
                    bytesWritten += 1
                else:
                    fileInput.close()
                    self.closePorts()
                    print "{0}::Read file complete, bytes read:{1}, bytes written:{2}".format(self.getName(), bytesRead, bytesWritten)     
                    break
        except IOError, e:
            print "{0}::Problem reading input data file::{1}".format(self.getName(), e)

if __name__ == "__main__":
    filter1 = SourceFilter("msg.txt")
    filter2 = SinkFilter()
    filter2.connect(filter1)
    filter1.start()
    filter2.start()
    