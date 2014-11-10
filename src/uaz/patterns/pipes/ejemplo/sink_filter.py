import datetime
import struct
from filter_framework import FilterFramework


class SinkFilter(FilterFramework):
    def __init__(self):
        FilterFramework.__init__(self)
        
        
    def run(self):
        timeStamp = 0
        timeStampFormat = "%Y %m %d::%H:%M:%S:%f"
        measurementLength = 8   # Esta es la longitud de todas las mediciones
        idLength = 4            # Esta es la longitud de los IDs en el flujo de bytes
        dataByte = 0            # Este es el byte leido del flujo
        bytesRead = 0           # Este es el numero de bytes leido del flujo
        measurement = 0         # Esta es la palabra usada para almacenar todas las mediciones, se muestran conversiones
        idMeasurement = 0                  # Este es el ID de medicion
        
        print "{0}::Sink reading".format(self.getName())
        
        while True:
            try:
                #############################################################################
                # Sabemos que el primer dato que entra al filtro va a ser un ID de longitud
                # idLength. Primero obtenemos los bytes del ID                
                #############################################################################               
                idMeasurement = 0
                i = 0
                while i < idLength:
                    dataByte = self.readByte() # Aqui leemos el byte del flujo
                    idMeasurement = idMeasurement << 8
                    idMeasurement = idMeasurement | dataByte                
                    bytesRead += 1
                    i += 1
                
                #############################################################################
                # Aqui leemos mediciones. Todos los datos de medicion se leen como un flujo de bytes
                # y se almacenan como un valor long. Esto nos permite hacer manipulaciones a nivel bit
                # que son necesarias para convertir el flujo de bytes en varias palabras da datos. Notese que
                # las manipulaciones de bits no estan permitidas en tipos de punto flotante en python.
                # Si el id = 0, entonces este es un valor de tiempo y por ello es un valor long - no
                # hay problema. Sin embargo, si el id es algo distinto a cero, entonces los bits
                # en el valor long son realmente de tipo double y necesitamos convertir el valor usando
                # la libreria struct para hacer la conversion, lo cual se muestra
                # abajo.
                #############################################################################
                measurement = 0
                i = 0
                while i < measurementLength:
                    dataByte = self.readByte()
                    measurement = measurement << 8
                    measurement = measurement | dataByte
                    bytesRead += 1
                    i += 1
                
                #############################################################################
                # Aqui buscamos un ID de 0 que indica que esta es una medicion de tiempo.
                # Cada marco (frame) empieza con un ID de 0 seguido de una estampa de tiempo
                # que correlaciona con el tiempo en que se registro la medicion. El tiempo es almacenado
                # en milisegundos desde Epoch. Esto nos permite usar la libreria datetime para
                # recuperar el tiempo y tambien usar metodos de formateo de texto para dar formato
                # a la salida en un formato legible para los humanos. Esto provee gran flexibilidad
                # en terminos de lidiar con el tiempo de forma aritmetica para propositos de 
                # despliegue de cadenas. Esto se ilustra abajo.
                #############################################################################
                if idMeasurement == 0:
                    timeStamp = datetime.datetime.fromtimestamp(measurement/1000.0)
                    
                    
                #############################################################################
                # Aqui tomamos una medicion (ID = 4 en este caso), pero se puede tomar cualquier
                # medicion que se quiera. Todas las mediciones en el flujo son recuperadas
                # por esta clase. Notese que todas las mediciones son de tipo double.
                # Esto ilustra como convertir los bytes leidos del flujo en un tipo double. 
                # Esto es bastante simple pasando el valor de tipo long a un arreglo de bytes
                # y despues pasandolo a un tipo double. Hay que tener cuidado aqui con el primer
                # parametro que se le pasa al metodo pack, esto indica los endianess que se usan,
                # esto es dependiente del procesador donde se este ejecutando. Puede considerar 
                # cambiarlo por ">Q" para big-endian o "<Q" para little endian, el "@Q" es para el nativo.
                #############################################################################
                if idMeasurement == 4:
                    #convertimos la medida de 8 bytes en un arreglo de 8 bytes
                    byteArray = struct.pack("@Q", measurement) 
                    #convertimos el arreglo de 8 bytes en un numero decimal
                    doubleValue = struct.unpack('d', byteArray)[0]
                    print "{0} -- ID = {1} {2}".format(timeStamp.strftime(timeStampFormat), idMeasurement, doubleValue)
            except:
                self.closePorts()
                print "{0}::Sink Exiting; bytes read: {1}".format(self.getName(), bytesRead)
                break