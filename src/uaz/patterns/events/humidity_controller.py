from event_package.event_manager_interface import EventManagerInterface
import sys
from instrumentation_package.message_window import MessageWindow
from instrumentation_package.indicator import Indicator
from event_package.event import Event
from time import sleep

def main():
    eventManager = None
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
        # Now we create the humidity control status and message panel
        # We put this panel about 2/3s the way down the terminal, aligned to the left
        # of the terminal. The status indicators are placed directly under this panel
        mw = MessageWindow("Humidity Controller Status Console", 0.0, 0.6)
        #Now we put the indicators directly under the humitity status and control panel
        hi = Indicator("Humid OFF", mw.getX(), mw.getY() + mw.getHeight())
        di = Indicator("DeHumid OFF", mw.getX() + hi.getWidth() * 2, mw.getY() + mw.getHeight() )
        mw.writeMessage("Registered with the event manager." )
        try:
            mw.writeMessage("   Participant id: " + str(eventManager.getMyId()) )
            mw.writeMessage("   Registration Time: " + eventManager.getRegistrationTime() )
        except Exception  as error:
            print "Error:: " + str(error)
        #end try
        done = False
        while not done:
            try:
                eventQueue = eventManager.getEventQueue()
            except Exception as error:
                mw.writeMessage("Error getting event queue::" + str(error))
            #end try
            
            # If there are messages in the queue, we read through them.
            # We are looking for EventIDs = 4, this is a request to turn the
            # humidifier or dehumidifier on/off. Note that we get all the messages
            # at once... there is a 2.5 second delay between samples,.. so
            # the assumption is that there should only be a message at most.
            # If there are more, it is the last message that will effect the
            # output of the humidity as it would in reality.
            while eventQueue.getSize() > 0:
                event = eventQueue.getEvent()
                if event.getEventId() == 4: 
                    if event.getMessage().upper() == "H1":
                        humidifierState = True
                        mw.writeMessage("Received humidifier on event")
                        # Confirm that the message was recieved and acted on
                        confirmMessage(eventManager, "H1")
                    elif event.getMessage().upper() == "H0":
                        humidifierState = False
                        mw.writeMessage("Received humidifier off event")
                        confirmMessage(eventManager, "H0")
                    elif event.getMessage().upper() == "D1":
                        dehumidifierState = True
                        mw.writeMessage("Received dehumidifier on event")
                        confirmMessage(eventManager, "D1")
                    elif event.getMessage().upper() == "D0":
                        dehumidifierState = False
                        mw.writeMessage("Receivied dehumidifier off event")
                        confirmMessage(eventManager, "D0")
                    #end if
                elif event.getEventId() == 99:
                    done = True
                    try:
                        eventManager.unRegister()
                    except Exception as error:
                        mw.writeMessage("Error unregistering: " + str(error))
                    mw.writeMessage("\n\nSimulation stopped. \n")
                    hi.close()
                    di.close()
                #end if
            #end while
            
            if humidifierState:
                # Set to green, humidifier is on
                hi.setLampColorAndMessage("HUMID ON", 1)
            else:
                # Set to gray, humidifier is off
                hi.setLampColorAndMessage("HUMID OFF", 0)
                
            if dehumidifierState:
                # Set to green, dehumidifier is on
                di.setLampColorAndMessage("DEHUMID ON", 1)
            else:
                # Set to gray, dehumidifier is off
                di.setLampColorAndMessage("DEHUMID OFF", 0)
            sleep(delay)
        #end while
    else:
        print "Unable to register with the event manager.\n\n"        
    #end if
#end def

def confirmMessage(eventManager, message):
    event = Event(-4, message)
    try:
        eventManager.sendEvent(event)
    except Exception as error:
        print "Error confirming message:: " + str(error) 
#end def

if __name__ == "__main__": main()
