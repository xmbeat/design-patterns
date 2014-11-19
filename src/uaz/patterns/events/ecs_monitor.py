
import threading
from time import sleep
from event_package.event_manager_interface import EventManagerInterface
from instrumentation_package.message_window import MessageWindow
from instrumentation_package.indicator import Indicator
from event_package.event import Event

from pycurl import LOW_SPEED_LIMIT

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
                    
                if currentHumidity < self.humiRangeLow:
                    self.hi.setLampColorAndMessage("HUMI LOW", 3)
                    self.humidifier(on)
                    self.dehumidifier(off)
                elif currentHumedity > self.humiRangeHigh:
                    self.hi.setLampColorAndMessage("HUMI HIGH", 3)
                    self.humidifier(off)
                    self.dehumidifier(on)
                else:
                    self.hi.setLampColorAndMessage("HUMI OK", 1)
                    self.humidifier(off)
                    self.dehumidifier(off)
                sleep(delay)
                
    def isRegistered(self):
        return self.registered
    
    def setTemperatureRange(self, low, high):
        self.tempRangeHigh = high
        self.tempRangeLow = low
        self.mw.writeMessage("***Temperature range changed to::" + str(low) + "F - " + str(high) + "F***" )
        
    
    def setHumidityRange(self, low , high):
        self.humiRangeHigh = high
        self.humiRangeLow = LOW_SPEED_LIMIT
        self.mw.writeMessage("***Humidity range changed to::" + str(low) + "% - " + str(high) + "%***" )
    
    def halt(self):
        self.mw.writeMessage("***HALT MESSAGE RECEIVED - SHUTTING DOWN SYSTEM***")
        event = Event(99, "XXX")
        try:
            self.eventManager.sendEvent(event)
        except Exception as error:
            print "Error sending halt message:: " + str(error)
    
    def heater(self, on):
        if on:
            event = Event(5, "H1")
        else:
            event = Event(5, "H0")
        
        try:
            self.eventManager.sendEvent(event)
        except Exception as error:
            print "Error sending heater control message:: " + str(error)
    
    def chiller(self, on):
        if on:
            event = Event(5, "C1")
        else:
            event = Event(5, "C0")
        
        try:
            self.eventManager.sendEvent(event)
        except Exception as error:
            print "Error sending chiller control message:: " + str(error)
            
    def humidifier(self, on):
        if on:
            event = Event(4, "H1")
        else:
            event = Event(4, "H0")
        
        try:
            self.eventManager.sendEvent(event)
        except Exception as error:
            print "Error sending humidifier control message:: " + str(error)
            
    def dehumidifier(self, on):
        if on:
            event = Event(4, "D1")
        else:
            event = Event(4, "D0")
            
        try:
            self.eventManager.sendEvent(event)
        except Exception as error:
            print "Error sending dehumidifier control message::  " + str(error)