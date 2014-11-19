from termio_package.termio import Termio
import sys
from ecs_monitor import ECSMonitor



if __name__ == "__main__":
    userInput = Termio()    # Termio IO Object
    done = False            # Main Loop Flag
    event = None            # Event Object
    error = False           # Error flag
    monitor = None          # The environmental control system monitor
    tempRangeHigh = 100.0   # These parameters signify the temperature and humidity ranges in terms 
    tempRangeLow = 0.0      # of high value and low values. The ECSmonitor will attempt to maintain
    humiRangeHigh = 100.0   # this temperature and humidity. Temperatures are in degrees Fahrenheit
    humiRangeLow = 0.0      # and humidity is in relative humidity percentage.
    
    # Get the IP address of the event manager
    if len(sys.argv) > 1:
        monitor = ECSMonitor(sys.argv[1]) 
    else:
        monitor = ECSMonitor()
             
    # Here we check to see if registration worked. If ef is null then the
    # event manager interface was not properly created.
    if monitor.isRegistered():            
        monitor.start()
        while not done:
            # Here, the main thread continues and provides the main menu
            print "\n\n\n"
            print "Environmental Control System (ECS) Command Console:\n"
            
            if len(sys.argv) > 1:
                print  "Using event manger at: " + sys.argv[1] + "\n"
            else:
                print "Using local event manger \n"
            
            print "Set  Range: " + str(tempRangeLow) + "F - " + str(tempRangeHigh) + "F"
            print "Set Humidity Range: " + str(humiRangeLow) + "% - " + str(humiRangeHigh) + "%\n"
            print "Select an Option: \n"
            print "1: Set temperature ranges" 
            print "2: Set humidity ranges"
            print "X: Stop System"
            print "\n >>>>"
            option = userInput.keyboardReadString()
            
            # === OPTION 1 ===
            if option == "1":
                # Here we get the temperature ranges
                error = True
                while error:
                    # Here we get the low temperature range
                    while error:
                        option = userInput.keyboardReadString("\nEnter the low temperature>>>")
                        if userInput.isNumber(option):
                            error = False
                            tempRangeLow = float(option)
                        else:
                            print "Not a number, please try again..."
                    
                    error = True
                    # Here we get the high temperature range
                    while error:
                        option = userInput.keyboardReadString("\nEnter the high temperature>>>")
                        if userInput.isNumber(option):
                            error = False
                            tempRangeHigh = float(option)
                        else:
                            print "Not a number, please try again..."
                    
                    if tempRangeLow >= tempRangeHigh:
                        print "\nThe low temperature range must be less than the high temperature range..."
                        print "Please try again...\n"
                        error = True
                    else:
                        monitor.setTemperatureRange(tempRangeLow, tempRangeHigh)
                        
            # === OPTION 2 ===       
            elif option == "2":
                # Here we get the humidity ranges
                error = True
                while error:
                    # Here we get the low humidity range
                    while error:
                        option = userInput.keyboardReadString("\nEnter the low humidity>>> ")
                        if userInput.isNumber(option):
                            error = False
                            humiRangeLow = float(option)
                        else:
                            print "Not a number, please try again..."
                    
                    error = True
                    # Here we get the high temperature range
                    while error:
                        option = userInput.keyboardReadString("\nEnter the high humidity>>> ")
                        if userInput.isNumber(option):
                            error = False
                            humiRangeHigh = float(option)
                        else:
                            print "Not a number, please try again..."
                    if humiRangeLow >= humiRangeHigh:
                        print "\nThe low humidity range must be less than the high humidity range..."
                        print "Please try again...\n"
                        error = True
                    else:
                        monitor.setHumidityRange(humiRangeLow, humiRangeHigh)
            # === OPTION X ===
            elif option.lower() == "x":
                
                # Here the user is done, so we set the Done flag and halt
                # the environmental control system. The monitor provides a method
                # to do this. Its important to have processes release their queues
                # with the event manager. If these queues are not relsasdeased these
                # become dead queues and they collect events and will eventually
                # cause problems for the event manager.
                monitor.halt()
                done = True
                print  "\nConsole Stopped... Exit monitor mindow to return to command prompt."
                
    else:
        print "\n\nUnable start the monitor.\n\n"