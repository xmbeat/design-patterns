
import time
class EventQueue(object):
    def __init__(self):
        self.eventList = []
        self.queueId = int(time.time() * 1000)

    def getId(self):
        return self.queueId
    
    def getSize(self):
        return len(self.eventList)
    
    def addEvent(self, event):
        self.eventList.append(event)
    
    def getEvent(self):
        event = None
        if len(self.eventList) > 0:
            event = self.eventList.pop(0)
        return event
    
    def clear(self):
        self.eventList = []
    
    def getCopy(self):
        copy = EventQueue()
        for i in self.eventList:
            copy.addEvent(i)
        return copy
    