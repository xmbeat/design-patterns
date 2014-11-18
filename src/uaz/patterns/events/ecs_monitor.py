
import threading
from time import sleep
from event_package.event_manager_interface import EventManagerInterface
from instrumentation_package.message_window import MessageWindow
from instrumentation_package.indicator import Indicator

class ECSMonitor(threading.Thread):
    def __init__(self, ipAddress = None):
        threading.Thread.__init__(self)
        self.registered = True
        self.tempRangeHigh = 100
        self.tempRangeLow = 0
        self.humiRangeHigh = 100
        self.humiRangeLow = 0
        try:
            self.eventManager = EventManagerInterface(ipAddress)
        except Exception as error:
            print "Error instantiating event manager interface: " + str(error)
            self.registered = False
            
    def run(self):
        if not self.eventManager is None:
           
            delay = 1.0     #The loop delay (1 second)      
            on = True       #Used to turn on heaters, chillers, humidifiers, and dehumidifiers
            off = False     #Used to turn off heaters, chillers, humidifiers, and dehumidifiers
            currentTemperature = 0
            currentHumedity = 0
            self.mw = MessageWindow("ECS Monitoring Console", 0, 0)
            self.ti = Indicator("TEMP UNK", self.mw.getX() + self.mw.getWidth(), 0)
            self.hi = Indicator("HUMI UNK", self.mw.getX() + self.mw.getWidth(), 
                                self.mw.getHeight() / 2, 2)
            self.mw.writeMessage("Registered with the Event Manager")
            try:
                self.mw.writeMessage("    Participant id: " + str(self.eventManager.getMyId()) )
                self.mw.writeMessage("    Registration time: " + str(self.eventManager.getRegistrationTime()) )
                
            except Exception as error:
                print "Error: " + str(error)
          
            done = False
            while not done:
                try:
                    eventQueue = self.eventManager.getEventQueue()
                except Exception as error:
                    self.mw.writeMessage("Error getting event queue::" + str(error))
                    
                while eventQueue.getSize() > 0:
                    event = eventQueue.getEvent()
                    if event.getEventId() == 1: #temperature reading
                        try:
                            currentTemperature = float(event.getMessage())
                        except Exception as error:
                            self.mw.writeMessage("Error reading temperature: " + str(error))
                    elif event.getEventId == 2: #humidity reading
                        try:
                            currentHumidity = float(event.getMessage())
                        except Exception as error:
                            self.mw.writeMessage("Error reading humidity: " + str(error))
                    elif event.getEventId == 99:
                        done = True
                        try:
                            self.eventManager.unRegister()
                        except Exception as error:
                            self.mw.writeMessage("Error unregistering: " + str(error))
                        self.mw.writeMessage("\n\nSimulation stopped. \n")
                        self.hi.close()
                        self.ti.close()
                    
                self.mw.writeMessage("Temperature:: " + str(currentTemperature) + "F humidity:: " + str(currentHumidity) )
                if currentTemperature < self.tempRangeLow:
                    self.ti.setLampColorAndMessage("TEMP LOW", 3)
                    self.heater(on)
                    self.chiller(off)
                elif currentTemperature > self.tempRangeHigh:
                    self.ti.setLampColorAndMessage("TEMP HGH", 3)
                    self.heater(off)
                    self.chiller(on)
                else:
                    self.ti.setLampColorAndMessage("TEMP OK", 1)
                    self.heater(off)
                    self.chiller(off)
                sleep(delay)
                
    def isRegistered(self):
        return self.registered
    
    def setTemperatureRange(self, low, high):
        pass
    
    def setHumidityRange(self, low , high):
        pass
        