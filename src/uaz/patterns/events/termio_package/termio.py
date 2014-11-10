
class Termio:
    def keyboardReadString(self, prompt = None):
        try:
            stringItem = raw_input(prompt)
            return stringItem
        except:
            print "Read Error in Termio.keyboardReadString method"
        return None
    
    def isNumber(self, stringItem):
        try:
            float(stringItem)
            return True
        except:
            return False
        
    def toInteger(self, stringItem):
        try:
            intItem = int(stringItem)
            return intItem
        except:
            print "Error converting " + str(stringItem) + " to a integer number::Termio.toInteger method"
            
    def toFloat(self, stringItem):
        try:
            floatItem = float(stringItem)
            return floatItem
        except:
            print "Error converting " + str(stringItem) + " to a floating point number::Termio.toFloat method"
            return 0.0