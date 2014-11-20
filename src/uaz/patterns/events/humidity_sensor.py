from event_package.event_manager_interface import EventManagerInterface
import sys
from instrumentation_package.message_window import MessageWindow
from event_package.event import Event
from time import sleep
import random

def main():
    try:
        # Get the IP address of the event manager
        if len(sys.argv) > 1:
            eventManager = EventManagerInterface(sys.argv[1])
        else:
            eventManager = EventManagerInterface()
    except Exception as error:
        print "Error instantiating event manager interface: " + str(error)
        
    # Here we check to see if registration worked. If eventManager is null then the
    # event manager interface was not properly created.
    if not eventManager is None:
        humidifierState = False
        dehumidifierState = False
        delay = 2.5        
        # We create a message window. Note that we place this panel about 1/2 across 
        # and 2/3s down the screen
        mw = MessageWindow("Humidity Sensor", 0.5, 0.6)
        
        mw.writeMessage("Registered with the event manager." )
        try:
            mw.writeMessage("   Participant id: " + str(eventManager.getMyId()) )
            mw.writeMessage("   Registration Time: " + eventManager.getRegistrationTime() )
        except Exception  as error:
            print "Error:: " + str(error)
        #end try
        mw.writeMessage("\nInitializing Humidity Simulation::")
        relativeHumidity = getRandomNumber() * 100.0
        
        if coinToss():
            driftValue = getRandomNumber() * -1.0
        else:
            driftValue = getRandomNumber()
        #end if
        
        mw.writeMessage("   Initial Humidity Set:: " + str(relativeHumidity) )
        mw.writeMessage("   Drift Value Set:: " + str(driftValue) )
        
        #********************************************************************
        #** Here we start the main simulation loop
        #********************************************************************
        mw.writeMessage("Beginning Simulation... ")
        
        done = False
        while not done:
            # Post the current relative humidity
            postHumidity(eventManager, relativeHumidity)
            mw.writeMessage("Current Relative Humidity:: " + str(relativeHumidity) + "%")
            try:
                eventQueue = eventManager.getEventQueue()
            except Exception as error:
                mw.writeMessage("Error getting event queue::" + str(error))
            #end try
            
            while eventQueue.getSize() > 0:
                event = eventQueue.getEvent()
                if event.getEventId() == -4:
                    if event.getMessage().upper() == "H1":
                        humidifierState = True
                    elif event.getMessage().upper() == "H0":
                        humidifierState = False
                    elif event.getMessage().upper() == "D1":
                        dehumidifierState = True
                    elif event.getMessage().upper() == "D0":
                        dehumidifierState = False
                    #end if
                # If the event ID == 99 then this is a signal that the simulation
                # is to end. At this point, the loop termination flag is set to
                # true and this process unregisters from the event manager.
                elif event.getEventId() == 99:
                    done = True
                    try:
                        eventManager.unRegister()
                    except Exception as error:
                        mw.writeMessage("Error unregistering: " + str(error))
                    #end try
                    mw.writeMessage("\n\nSimulation stopped. \n")
                #end if
            #end while
            
            # Now we trend the relative humidity according to the status of the
            # humidifier/dehumidifier controller.
            # Humidifier is on
            if humidifierState:
                relativeHumidity += getRandomNumber()
            # if both the humidifier and dehumidifier are off
            if (not humidifierState) and (not dehumidifierState):
                relativeHumidity += driftValue
            # if dehumidifier is on
            if dehumidifierState:
                relativeHumidity -= getRandomNumber()
            
            sleep(delay)            
        #end while
    else:
        print "Unable to register with the event manager.\n\n"        
    #end if
#end def


# CONCRETE FUNCTION:: getRandomNumber
# Purpose: This method provides the simulation with random floating point
#           humidity values between 0.1 and 0.9.
def getRandomNumber():
    return random.random() * 0.9 + 0.1
#end def

# CONCRETE METHOD:: CoinToss
# Purpose: This method provides a random true or false value used for
# determining the positiveness or negativeness of the drift value.
def coinToss():
    return random.choice([True, False, True, False, True, False])
#end def


def postHumidity(eventManager, humidity):
    event = Event(2, str(humidity))
    try:
        eventManager.sendEvent(event)
    except Exception as error:
        print "Error posting relative humidity:: " + str(error)
    #end try
#end def

if __name__ == "__main__": main()