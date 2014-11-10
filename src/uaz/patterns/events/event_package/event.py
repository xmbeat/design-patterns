class Event:
    def __init__(self, eventId, message = None):
        self.eventId = eventId
        self.message = message
        self.senderId = 0
        
    def getSenderId(self):
        return self.senderId
    
    def setSenderId(self, senderId):
        self.senderId = senderId
    
    def getEventId(self):
        return self.eventId
    
    def getMessage(self):
        return self.message