from filter_framework import FilterFramework

class SourceFilterTemplate(FilterFramework):
    def __init__(self):
        FilterFramework.__init__(self)
        
    def run(self):
        # * Este es el ciclo principal de procesamiento para el filtro.
        # * Puesto que es un filtro fuente, el programador debe determinar
        # * cuando acaba el ciclo.
        while True:
            # * El programador puede insertar codigo para las operaciones del filtro
            # * aqui incluyendo la lectura de datos de algun archivo o dispositivo.
            # * Notese que independientemente de la manera en que se leen los datos,
            # * los datos deben ser enviados un byte a la vez a la tuberia de salida. Esto se ha
            # * hecho para adherir al paradigma de filtros y tuberias y
            # * proveer un alto grado de portabilidad entre filtros.
            # * Sin embargo, tu debes convertir datos de entrada a algo de tipo byte por ti
            # * mismo. La siguiente linea de codigo escribe un byte de datos al puerto
            # * de salida del filtro. Si se sale del ciclo, se debe llamar closePorts() para
            # * cerrar los puertos del filtro de manera ordenada. Esto se muestra adelante
            # * aunque esta comentado. En donde se cierran los puertos depende de donde
            # * se termine el ciclo
            data = 0
            self.writeByte(data)
        
        #self.closePorts()