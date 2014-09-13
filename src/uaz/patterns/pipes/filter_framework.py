import threading
from time import sleep

class PipedOutputStream:
    def __init__(self):
        self.__sink = None
        self.__cond = threading.Condition()
    
    def connect(self, sink):
        self.__cond.acquire()
        if sink is None:
            self.__cond.release()
            raise Exception("Null pointer exception")
        elif (self.__sink is not None or sink.__connectedon):
            raise Exception("Already connected")
            self.__cond.release()
        self.__sink = sink
        sink.__in = -1
        sink.__out = 0
        sink.__connected = True
        self.__cond.release()
    
    def write(self, data):
        if (self.__sink is None):
            raise Exception("Pipe not connected")
        self.__sink.__receive__(data)
        
    def flush(self):
        sink = self.__sink
        if sink is not None:
            sink.__cond.acquire()
            sink.__cond.notifyAll()
            sink.__cond.release()
    
    def close(self):
        sink = self.__sink
        if sink is not None:
            sink.__received_last__()
            
class PipedInputStream:
    def __init__(self):
        self.__buffer = bytearray()
        self.__cond = threading.Condition()
        self.__in = -1
        self.__out = 0
        self.__connected = False
        self.__close_by_reader = False #Volatile
        self.__close_by_writer = False
        self.__read_side = None
        self.__write_side = None
        
    def connect(self, src):
        src.connect(self)
    
    def close(self):
        self.__close_by_reader = True
        self.__cond.acquire()
        self.__in = -1
        self.__cond.release()
        
    def read(self):
        if not self.__connected:
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
            self.__cond.notifyAll()
            self.__cond.wait(1000)
        
        self.__out += 1
        ret = buffer[self.__out]
        
        if (self.__out >= len(self.__buffer)):
            self.__out = 0;

        if (self.__in == self.__out):
            # now empty 
            self.__in = -1;

        return ret;
       
    def available(self):
        self.__cond.acquire()      
        if self.__in < 0:
            aux = 0
        elif self.__in == self.__out:
            aux =  len(self.__buffer)
        elif self.__in > self.__out:
            aux = self.__in - self.__out;
        else:
            aux = self.__in + len(self.__buffer) - self.__out;
        self.__cond.release()
        return aux
    
    def __check_state__(self):
        if self.__connected == False:
            raise Exception("Pipe not connected")
        elif self.__close_by_reader or self.__close_by_writer:
            raise Exception("Pipe closed")
        elif (self.__read_side is not None) and (not self.__read_side.isAlive()):
            raise Exception("Read end dead")
        
    def __await_space__(self):
        while self.__in == self.__out:
            self.__check_state__()
            # full: kick any waiting readers
            self.__cond.notifyAll()
            self.__cond.wait(1000)
    
    def __receive__(self, b):
        self.__cond.acquire()
        self.__check_state__()
        self.__write_side = threading.current_thread()
        
        if (self.__in == self.__out):
            self.__await_space__()
            
        if (self.__in < self.__out):
            self.__in = 0
            self.__out = 0
        
        self.__buffer[self.__in] = b
        self.__in += 1
        
        if (self.__in >= len(self.__buffer)):
            self.__in = 0
    
    def __receive_last__(self):
        self.__cond.acquire()
        self.__close_by_writer = True
        self.__cond.notify_all()
        self.__cond.release()
    
class FilterFramework(threading.Thread):
    def connect(self, filter_framework):
        try:
            # Connect this filter's input to the upstream pipe's output stream
            self.input_read_port.connect(filter_framework.output_write_port)
            self.input_filter = filter_framework
        except BaseException, error:
            print "\n{0} FilterFramework error connecting::{1}".format(self.getName(), error)
                      
    def read_byte(self):
        try:
            while self.input_read_port.available() == 0:
                if self.end_of_input_stream():
                    raise EndOfStreamException("End of input stream reached")
                sleep(0.250)
        except EndOfStreamException, error:
            raise error
        except Exception, error:
            print "\n{0} Error in read port wait loop::{1}".format(self.getName(), error)
        try:
            data = self.input_read_port.read()
            return data
        except Exception, error:
            print "\n{0} Pipe read error::{1}", self.getName(), error
            return 0
    
    def write_byte(self, data):
        try:
            self.output_write_port.write(data)
            self.output_write_port.flush()
        except Exception, error:
            print "\n{0} Pipe write error::{1}".format(self.getName(), error)
            
    def end_of_input_stream(self):
        return not self.input_filter.isAlive()
    
    def close_ports(self):
        try:
            self.input_read_port.close()
            self.output_write_port.close()
        except Exception, error:
            print "\n{0} close_ports error::{1}".format(self.getName(), error)
                
class EndOfStreamException(Exception):
    def __init__(self, message = None):
        Exception.__init_(self)
        self.message = message


class MiddleFilter(FilterFramework):
    
    def run(self):
        read = 0        #Cantidad de bytes leidos
        written = 0     #Cantidad de bytes escritos
        data = 0        #El byte leido de la entrada

        #A continuacion un mensaje a la terminal para avisar al mundo que estamos vivo...
        print "\n{0}::Middle Reading ".format(self.getName())

        while (True):
            ##########################################################
            #    Aqui leemos un byte y escribimos un byte
            ##########################################################
            try:
                data = self.read_byte()
                read += 1
                self.write_byte(data)
                written += 1
            except EndOfStreamException:
                self.close_ports()
                print "\n{0}::Middle Exiting; bytes read: {1}, bytes written{2}".format(self.getName(), read, written)
                break
            