from uaz.patterns.pipes.filter_framework import FilterFramework, EndOfStreamException

class MiddleFilter(FilterFramework):
    
    def run(self):
        read = 0        #Cantidad de bytes leidos
        written = 0     #Cantidad de bytes escritos
        data = 0        #El byte leido de la entrada

        #A continuacion un mensaje a la terminal para avisar al mundo que estamos vivos...
        print "{0}::Middle Reading ".format(self.getName())

        while (True):
            ##########################################################
            #        Aqui leemos un byte y escribimos un byte
            ##########################################################
            try:
                data = self.readByte()
                read += 1
                self.writeByte(data)
                written += 1                
                #print "MiddleBytesWritten:" + str(written)
            except EndOfStreamException:
                self.closePorts()
                print "{0}::Middle Exiting; bytes read: {1}, bytes written: {2}".format(self.getName(), read, written)
                break
                