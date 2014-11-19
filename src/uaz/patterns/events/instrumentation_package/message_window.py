import Tkinter as gui
import Pmw
import time
from datetime import datetime
import threading
from time import sleep

class MessageWindow(gui.Frame):
    
    def _safeInit(self, title, xPos, yPos, master = None):
        gui.Frame.__init__(self, gui.Tk(), background="blue")
        screenW = self.master.winfo_screenwidth()
        screenH = self.master.winfo_screenheight()        
        windowW = screenW * 0.5
        windowH = screenH * 0.25       
       
        self.messageArea = Pmw.ScrolledText(self, borderframe=1,
                                usehullsize=1,
                                hull_width=400, hull_height=300,
                                text_padx=10, text_pady=10,
                                text_wrap='none')                                
        self.messageArea.pack(fill=gui.BOTH, expand=1, padx=5, pady=5)        
        self.pack(fill=gui.BOTH, expand=1)
        self.master.geometry('%dx%d+%d+%d' % (windowW, windowH, xPos, yPos))        
        self.master.title(title)
        self.running[0] = True
        self.bind("<Destroy>", lambda widget: (self.running.pop(), widget.widget.destroy()))
        self.master.mainloop()
        
    def __init__(self, title, xPos, yPos, master = None):
        self.running = [False]
        thread = threading.Thread(target=MessageWindow._safeInit, args=(self, title, xPos, yPos, master))
        thread.start()
        self._isAlive()
        
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
        
    def _safeWriteMessage(self, message):
        
        timeStamp = datetime.fromtimestamp(time.time())
        timeString = timeStamp.strftime("%Y/%m/%d::%H:%M:%S:%f")
        timeString = timeString + "::" + message + "\n"
       
        self.messageArea.insert(gui.END, timeString)
        pos = self.messageArea.index(gui.END)
        self.messageArea.see(pos)
        #self.messageArea.mark_set(gui.END, "%d.%d" % (0,0))
    
    def _isAlive(self):
        if self.running:
            while self.running[0] == False:
                sleep(0)
            return True
        return False
    
    def writeMessage(self, message):
        if self._isAlive():
            self.after_idle(MessageWindow._safeWriteMessage, self, message)
        else:
            print "MessageWindow has been destroyed, can't write: " + message + "\n"
            
    def close(self):
        self.after_idle(self.master.destroy)
        
if __name__ == "__main__":
    m = MessageWindow("Hola", 0, 0)
    for i in range(1, 20):
        m.writeMessage("Hola mundo: " + str(i))
        m.getX()
        sleep(1)
    
    