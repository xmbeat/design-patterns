
import time
from datetime import datetime
import threading
from time import sleep

from gui import GUI
import gtk

class MessageWindow():
    def __init__(self, title, xPos, yPos):
        GUI.start()
        GUI.doOperation(self.createWidgets, title, xPos, yPos)
        
    def createWidgets(self, title, xPos, yPos):
        self.win = gtk.Window()
        GUI.windowCount += 1
        screen = self.win.get_screen()
        screenW = screen.get_width()
        screenH = screen.get_height()
        windowW = int(screenW * 0.5)
        windowH = int(screenH * 0.25)
        if type(xPos) is float:
            xPos = int(screenW * xPos)
        if type(yPos) is float:
            yPos = int(screenH * yPos)
        
        self.messageArea = gtk.TextView()
        self.win.set_size_request(windowW, windowH)
        self.win.set_title(title)
        self.win.show_all()
        self.win.move(xPos, yPos)
        color = gtk.gdk.Color(red = 0, green = 0,  blue = 255*256)
        self.win.modify_bg(gtk.STATE_NORMAL, color)
        self.win.connect("destroy", GUI.onDestroyWindow)
    def writeMessage(self, message):
        pass
    
    def getX(self):
        self.xPos = None
        def operation():
            x, y = self.win.get_position()
            self.xPos = x
        GUI.doOperation(operation)
        while self.xPos is None:
            sleep(0)
        return self.xPos
    
    def getY(self):
        self.yPos = None
        def operation():
            x, y = self.win.get_position()
            self.yPos = y
        GUI.doOperation(operation)
        while self.yPos is None:
            sleep(0)
        return self.yPos
    
    def getWidth(self):
        self.width = None
        def operation():
            width, height = self.win.get_size()
            self.width = width
        GUI.doOperation(operation)
        while self.width is None:
            sleep(0)
        return self.width
    
    def getHeight(self):
        self.height = None
        def operation():
            width, height = self.win.get_size()
            self.height = height
        GUI.doOperation(operation)
        while self.height is None:
            sleep(0)
        return self.height
    
    def close(self):
        def operation():
            self.win.destroy()
        GUI.doOperation(operation)

"""
class MessageWindow2(gui.Frame):
    
    def _safeInit(self, title, xPos, yPos, master = None):
        gui.Frame.__init__(self, gui.Tk(), background="blue")
        screenW = self.master.winfo_screenwidth()
        screenH = self.master.winfo_screenheight()        
        windowW = screenW * 0.5
        windowH = screenH * 0.25
          
        if type(xPos) is float:
            xPos = int(screenW * xPos)
        if type(yPos) is float:
            yPos = int(screenH * yPos)
            
        self.messageArea = Pmw.ScrolledText(self, borderframe=1,
                                usehullsize=1,
                                hull_width=400, hull_height=300,
                                text_padx=10, text_pady=10,
                                text_wrap='none')
                                  
        self.messageArea.pack(fill=gui.BOTH, expand=1, padx=5, pady=5)        
        self.pack(fill=gui.BOTH, expand=1)
        self.master.geometry('%dx%d+%d+%d' % (windowW, windowH, xPos, yPos))        
        self.master.title(title)
        def setRunning():
            self.running[0] = True
        self.after_idle(setRunning)
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
    """
if __name__ == "__main__":
    m = MessageWindow("Hola", 0, 0)
    for i in range(1, 20):
        m.writeMessage("Hola mundo: " + str(i))
        m.getX()
        sleep(1)
    
    