
import threading
from uaz.patterns.events.event_package.event_manager_interface import EventManagerInterface
from time import sleep

class ECSMonitor(threading.Thread):
    def __init__(self, ipAddress = None):
        threading.Thread.__init__(self)
        try:
            self.eventManager = EventManagerInterface(ipAddress)
        except Exception as error:
            print "Error instantiating event manager interface: " + str(error)
            
    def run(self):
        if self.eventManager:
            print "    Participant ID: " + str(self.eventManager.getMyId())
            print "    Registration Time: " + self.eventManager.getRegistrationTime()
            done = False
            while not done:
                eventQueue = self.eventManager.getEventQueue()
                while eventQueue.getSize() > 0:
                    event = eventQueue.getEvent()
                    if event.getEventId() == 99:
                        done = True
                        self.eventManager.unRegister()
                sleep(1)
                
    def isRegistered(self):
        return True
    
    def setTemperatureRange(self, low, high):
        pass
    
    def setHumidityRange(self, low , high):
        pass
        