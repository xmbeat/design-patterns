from uaz.patterns.pipes.source_filter import SourceFilter
from uaz.patterns.pipes.middle_filter import MiddleFilter
from uaz.patterns.pipes.sink_filter import SinkFilter

if __name__ == "__main__":
    filter1 = SourceFilter("msg.txt")
    filter2 = MiddleFilter()
    filter3 = SinkFilter()
    
    filter3.connect(filter2)
    filter2.connect(filter1)
    
    filter1.start()  
    filter2.start()    
    filter3.start()
      
    filter1.join()
    filter2.join()
    filter3.join()