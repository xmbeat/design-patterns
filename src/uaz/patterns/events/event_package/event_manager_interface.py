import Pyro4
import datetime
class ParticipantNotRegisteredException(Exception):
    pass

class EventManagerInterface:
    def __init__(self, ipAddress = None, port = 1099):
        if ipAddress == None:
            ipAddress = "localhost"
            
        Pyro4.config.SERIALIZER = 'pickle'
        Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
        
        server = "PYRO:EventManager@" + ipAddress + ":" + str(port)
        self.eventManager = Pyro4.Proxy(server)
        self.participantId = self.eventManager.register()
    
    def getMyId(self):
        self.checkParticipantId()
        return self.participantId
    
    def getRegistrationTime(self):
        self.checkParticipantId()
        timeStamp = datetime.datetime.fromtimestamp(self.participantId / 1000.0)
        return timeStamp.strftime("%Y %m %d::%H:%M:%S:%f")
    
    def sendEvent(self, event):
        self.checkParticipantId()
        event.setSenderId(self.participantId)
        self.eventManager.sendEvent(event)
        
    def getEventQueue(self):
        self.checkParticipantId()
        eventQueue = self.eventManager.getEventQueue(self.participantId)
        return eventQueue
    
    def unRegister(self):
        self.checkParticipantId()
        self.eventManager.unRegister(self.participantId)
        
        
    def checkParticipantId(self):
        if self.participantId == -1:
            raise  ParticipantNotRegisteredException("Participant not registered")
            