from source_filter import SourceFilter
from middle_filter import MiddleFilter
from sink_filter import SinkFilter

if __name__ == "__main__":
    filter1 = SourceFilter("../FlightData.dat")
    filter2 = MiddleFilter()
    filter3 = SinkFilter()
    
    filter3.connect(filter2)
    filter2.connect(filter1)
    
    filter1.start()  
    filter2.start()    
    filter3.start()
