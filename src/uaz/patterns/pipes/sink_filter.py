from uaz.patterns.pipes.filter_framework import FilterFramework

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