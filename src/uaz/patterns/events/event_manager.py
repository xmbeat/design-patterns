import Pyro4
from event_package.event_queue import EventQueue
import threading

class EventManager(object):
    def __init__(self):
        self.logger = EventManager.RequestLogger(self)
        self.eventQueueList = []
        self.cond = threading.Condition() #Para propositos de sincronizacion
    
    def register(self):
        self.cond.acquire()
        try:
            eventQueue = EventQueue()
            self.eventQueueList.append(eventQueue)
            self.logger.displayStatistics("Register event. Issued ID = " + str(eventQueue.getId()))     
            return eventQueue.getId()
        except Exception as error:
            self.logger.displayStatistics("WARNING::Register::" + str(error))       
        finally:
            self.cond.release()
    
    def unRegister(self, queueId):
        self.cond.acquire()
        try:
            found = False
            i = 0
            while i < len(self.eventQueueList) and not found :
                eventQueue = self.eventQueueList[i]
                if eventQueue.getId() == queueId:
                    self.eventQueueList.pop(i)
                    found = True
                i += 1
            
            if found:
                self.logger.displayStatistics( "Unregistered ID::" + str(queueId) );
            else:
                self.logger.displayStatistics( "Unregister error. ID:" + str(queueId) + " not found.");
        except Exception as error:
            self.logger.displayStatistics("WARNING::UnRegister::" + str(error))       
        finally:
            self.cond.release()
        
    def sendEvent(self, event):
        self.cond.acquire()
        try:
            for eventQueue in self.eventQueueList:
                eventQueue.addEvent(event)
            self.logger.displayStatistics("Incoming event posted from ID: " + str(event.getSenderId()))
        except Exception as error:
            self.logger.displayStatistics("WARNING::sendEvent::" + str(error))    
        finally:
            self.cond.release()
        
    def getEventQueue(self, queueId):
        self.cond.acquire()
        try:
            queue = None
            found = False
            i = 0
            while i < len(self.eventQueueList) and not found:
                eventQueue = self.eventQueueList[i]
                if eventQueue.getId() == queueId:
                    queue = eventQueue.getCopy()
                    eventQueue.clear()
                    found = True
                i += 1
            if found:
                self.logger.displayStatistics( "Get event queue request from ID: " + str(queueId) + ". Event queue returned.")
            else:
                self.logger.displayStatistics( "Get event queue request from ID: " + str(queueId) + ". ID not found.")
            
            return queue
        except Exception as error:
            self.logger.displayStatistics("WARNING::getEventQueue::" + str(error)) 
        finally:
            self.cond.release()
        
            
    class RequestLogger():
        def __init__(self, container):
            self.requestsServiced = 0 #This is the number of requests seviced   
            self.container = container        
            
        def displayStatistics(self, message):
            self.requestsServiced += 1
            print "-------------------------------------------------------------------------------"
            if len(message) > 0:
                print "Message: {0}".format(message)
                
            print "Number of requests: {0}".format(self.requestsServiced)
            print "Number of registered participants: {0}".format(len(self.container.eventQueueList))
            print "-------------------------------------------------------------------------------"
            
if __name__ == "__main__":
    try:    
        Pyro4.config.SERIALIZER = 'pickle'
        Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
        em = EventManager()
        daemon = Pyro4.Daemon(None, 1100)
        uri = daemon.register(em, "EventManager")
        print "EventManager Ready on => " + daemon.locationStr
        print "URI => " + str(uri)
        daemon.requestLoop()
        
    except Exception as error:
        print "EventManager startup error: " + str(error)