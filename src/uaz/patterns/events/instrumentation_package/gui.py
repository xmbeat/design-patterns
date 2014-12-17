import pygtk
import gobject
from time import sleep
pygtk.require('2.0')
import gtk
import threading
   
class GUI:
    _isGtkStarted = False
    _semaphore = threading.Condition()
    windowCount = 0
    
    @staticmethod
    def onDestroyWindow(widget):
        GUI.windowCount -= 1
        if (GUI.windowCount <= 0):
            gtk.main_quit()
        return True
    
    @staticmethod
    def doOperation(function, *args, **kw):
        def idle_func():
            gtk.threads_enter()
            try:
                function(*args, **kw)
                return False
            finally:
                gtk.threads_leave()
        gobject.idle_add(idle_func)
    
    @staticmethod
    def start():
        GUI._semaphore.acquire()
        if GUI._isGtkStarted == False:
            mainThread = threading.Thread(target= GUI.gtkThread)
            mainThread.start()
            #Esperamos a que el hilo haya comenzado el main loop
            while GUI._isGtkStarted == False:
                sleep(0)
        GUI._semaphore.release()
        
    @staticmethod
    def gtkThread():
        gtk.threads_init()
        
        #Esta funcion se ejecuta dentro del main loop, sirve para indicar que ya se ha iniciado el bucle
        def setRunning():
            GUI._isGtkStarted = True
        gobject.idle_add(setRunning)
        gtk.threads_enter()
        gtk.main()
        GUI._isGtkStarted = False
        gtk.threads_leave()