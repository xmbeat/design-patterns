import pygtk
pygtk.require('2.0')
import gtk
from gui import GUI
from time import sleep
import math
import cairo

class Indicator():
    
    def __init__(self, message, xPos, yPos, initColor=0):
        GUI.start()
        GUI.doOperation(Indicator.createWidgets, self , message, xPos, yPos, initColor)        
    
    def createWidgets(self, message, xPos, yPos, initColor):
        self.win = gtk.Window()
        GUI.windowCount += 1
        screen = self.win.get_screen()
        screenW = screen.get_width()
        screenH = screen.get_height()
        if screenW > screenH:
            self.height = int(screenH * 0.1)
        else:
            self.height = int(screenW * 0.1)
        
        if type(xPos) is float:
            xPos = int(screenW * xPos)
        if type(yPos) is float:
            yPos = int(screenH * yPos)
        self.colors = ([0.3, 0.3, 0.3], [0.0, 1.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0])
        self.iluminationColor = self.colors[initColor]
        self.message = message
        self.canvas = gtk.DrawingArea()        
        self.canvas.connect("expose-event", self.onDraw)
        self.win.add(self.canvas)
        self.win.set_resizable(False)
        self.win.set_size_request(self.height, self.height)
        self.win.show_all()
        self.win.move(xPos, yPos)
        self.win.set_title("Indicator")
        self.win.connect("destroy", GUI.onDestroyWindow)
    
    
 
    
    def onDraw(self, widget, event):
        w = self.win.allocation.width
        h = self.win.allocation.height
        context = widget.window.cairo_create()
        context.set_source_rgb(0, 0, 0)
        context.set_line_width(2)
        context.translate(w/2, h/2)
        
        context.arc(0, 0, h/2, 0, math.pi*2)
        context.stroke_preserve()
        
        context.set_source_rgb(self.iluminationColor[0], self.iluminationColor[1], self.iluminationColor[2])
        context.fill_preserve()
        
    
        context.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_size(10)
        textExtents = context.text_extents(self.message)
        context.move_to(-textExtents[2]/2, textExtents[3]/2)
        context.set_source_rgb(0, 0, 0)
        context.show_text(self.message)
    
    def setLampColorAndMessage(self, message, color):
        def operation():
            self.message = message
            self.iluminationColor = self.colors[color]
            self.canvas.queue_draw()
        GUI.doOperation(operation)
    
    def setLampColor(self, color):
        def operation():
            self.iluminationColor = self.colors[color]
            self.canvas.queue_draw()
        GUI.doOperation(operation)
        
    def setMessage(self, message):
        def operation():
            self.message = message
            self.canvas.queue_draw()
        GUI.doOperation(operation)
        
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
        