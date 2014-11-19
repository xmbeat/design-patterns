import Tkinter as gui
import Pmw
import threading
from time import sleep
from message_window import MessageWindow

class Indicator(gui.Frame):
    def __init__(self, message, xPos, yPos, initColor = 0):
        self.running = [False]
        thread = threading.Thread(target=Indicator._safeInit, args=(self, message, xPos, yPos, initColor))
        thread.start()
        self._isAlive()
        
    def _safeInit(self, message, xPos, yPos, initColor = 0):
        gui.Frame.__init__(self, gui.Tk())
        screenW = self.master.winfo_screenwidth()
        screenH = self.master.winfo_screenheight()
        if screenW > screenH:
            self.height = screenH * 0.1
        else:
            self.height = screenW * 0.1
        
        self.colors = ("black", "green", "yellow", "red")
        self.iluminationColor = self.colors[initColor]
        self.message = message
        
        self.pack(fill=gui.BOTH, expand=1)
        self.canvas = gui.Canvas(self)
        self.canvas.pack(fill=gui.BOTH, expand=1)
        self.master.geometry('%dx%d+%d+%d' % (self.height, self.height, xPos, yPos))
        self.repaint()
        self.master.title("Indicator")
        self.bind("<Destroy>", lambda widget: (self.running.pop(), widget.widget.destroy()))        
        self.running[0] = True
        self.master.mainloop()
        
    def _isAlive(self):
        if self.running:
            while self.running[0] == False:
                sleep(0) #Yield this thread
            return True
        return False
    
    def repaint(self):
        self.canvas.delete("all")
        
        self.canvas.create_oval(1,1,self.height-2, self.height-2, fill=self.iluminationColor)
        
        self.canvas.create_text(self.height / 2.0, self.height / 2, text=self.message)
      
        
    def _safeSetLampColorAndMessage(self, message, color):
        self.iluminationColor = self.colors[color]
        self.message = message
        self.repaint()
        
    def setLampColorAndMessage(self, message, color):
        if self._isAlive():
            self.after_idle(Indicator._safeSetLampColorAndMessage, self, message, color)
        else:
            print "Indicator has been destroyed, can't write: " + message + "\n"
    
    def _safeSetLampColor(self, color):
        self.iluminationColor = self.colors[color]
        self.repaint()
     
    def setLampColor(self, color):
        if self._isAlive():
            self.after_idle(Indicator._safeSetLampColor, self, color)
        else:
            print "Indicator has been destroyed, can't change color\n"
       
    
    def _safeSetMessage(self, message):
        self.message = message
        self.repaint()
    
    def setMessage(self, message):
        if self._isAlive():
            self.after_idle(Indicator._safeSetMessage, self, message)
        else:
            print "Indicator has been destroyed, can't set message: " + message + "\n"
            
    def _updateDimensions(self):
        self.x = self.master.winfo_x()
        self.y = self.master.winfo_y()
        self.width = self.master.winfo_width()
        self.height = self.master.winfo_height()
        self._isUpdateDimensions = True
    
    def _waitForUpdate(self):
        self._isUpdateDimensions = False
        self.after_idle(self._updateDimensions)
        while self._isUpdateDimensions == False:
            sleep(0)
    
    def getX(self):
        self._waitForUpdate()
        return self.x      
    
    def getY(self):
        self._waitForUpdate()
        return self.y
    
    def getHeight(self):
        self._waitForUpdate()
        return self.height
    
    
    def getWidth(self):
        self._waitForUpdate()
        return self.width
    
    def close(self):
        self.after_idle(self.master.destroy)
        
    