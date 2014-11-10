from filter_framework import FilterFramework

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
                    if bytesWritten == 1023:
                        pass
                    self.writeByte(data)
                    bytesWritten += 1
                    #print "SourceBytesWritten:" + str(bytesWritten)
                else:
                    fileInput.close()
                    self.closePorts()
                    print "{0}::Read file complete, bytes read:{1}, bytes written:{2}".format(self.getName(), bytesRead, bytesWritten)     
                    break
        except IOError, e:
            print "{0}::Problem reading input data file::{1}".format(self.getName(), e)

