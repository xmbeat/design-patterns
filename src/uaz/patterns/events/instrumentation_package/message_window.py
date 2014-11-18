import Tkinter as gui
import Pmw
import time
from indicator import Indicator
from datetime import datetime

class MessageWindow(gui.Frame):
    def __init__(self, title, xPos, yPos, master = None):
        gui.Frame.__init__(self,background="blue")
        
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
        
    
    def getX(self):
        return self.master.winfo_x()
    
    def getY(self):
        return self.master.winfo_y()
    
    def getHeight(self):
        return self.master.winfo_height()
    
    def getWidth(self):
        return self.master.winfo_width()
    
    def writeMessage(self, message):
        
        timeStamp = datetime.fromtimestamp(time.time())
        timeString = timeStamp.strftime("%Y/%m/%d::%H:%M:%S:%f")
        self.messageArea.appendtext(timeString + "::" + message + "\n")
        pos = self.messageArea.index(gui.END)
        
        self.messageArea.mark_set(gui.END, "%d.%d" % (0,0))
        
    def mainloop(self):
        
        gui.Frame.mainloop(self)  
if __name__ == "__main__":
    m = MessageWindow("Hola", 0, 0)
    w = Indicator("On", 0, 0, 0)
    m.writeMessage("Hola mundo")
    w.mainloop()
    
    
    