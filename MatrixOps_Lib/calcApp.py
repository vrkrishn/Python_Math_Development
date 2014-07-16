from utilityFuncs import *
from basicOps import *
from matrixSolver import *
from statsOps import *
from Tkinter import *
import time
import random

class CalculatorApp(object):
    def __init__(self,sideLength,unitSize):
        super(CalculatorApp,self).__init__()
        root = Tk()
        canvas = Canvas(root,width = sideLength,height = sideLength)
        self.canvas = canvas
        self.cHeight = sideLength
        self.cWidth = sideLength
        self.unitSize = unitSize
        self.canvas.pack()
        self.width = sideLength/unitSize
        self.height = sideLength/unitSize
        #Zoom Controls
        self.minZoom = -3
        self.maxZoom = 3
        self.zLevel = 0
        self.zStandard = 0
        self.zStep = 2
        #Initialize Uninherant Variables
        self.screens = dict()
        self.primaryScreen = "graph"
        self.drawScreens = []
        self.bounds = (0,0,0,0)
        self.addScreen("BG","graph",0,0,self.cWidth,self.cHeight,1,"NW",color = "grey")
        self.setScreenAbove("BG")
        self.action()
        self.redrawAllWrapper()
        self.run(root)
        
    #CONTROLLER FUNCTIONS
    
    def redrawAllWrapper(self):
        self.canvas.delete(ALL)
        self.redrawAll()
        
    def mousePressedWrapper(self,event):
        self.mousePressed(event)

    def keyPressedWrapper(self,event):
        self.keyPressed(event)
        
    def redrawAll(self):
        for screen in self.drawScreens:
            screen.draw()
        
    def mousePressed(self,event):
        pass
        
    def keyPressed(self,event):
        pass
        
    def run(self,root):
        root.bind("<Button-1>",self.mousePressedWrapper)
        root.bind("<Key>",self.keyPressedWrapper)
        root.mainloop()
    
    def zoomIn(self):
        if(self.zLevel < self.maxZoom):
            self.zLevel += 1
            self.unitSize *= self.zStep
            self.height /= self.zStep
            self.width /= self.zStep
        self.redrawAllWrapper()
        
    def zoomOut(self):
        if(self.zLevel > self.minZoom):
            self.zLevel -=1
            self.unitSize /= self.zStep
            self.height *= self.zStep
            self.width *= self.zStep
        self.redrawAllWrapper()
        
    def zoomStandard(self):
        zNeeded = self.zLevel-self.zStandard
        if (zNeeded > 0):
            for i in xrange(zNeeded):
                self.zoomOut()
        elif (zNeeded < 0):
            for i in xrange(abs(zNeeded)):
                self.zoomIn()
        
    # MODEL FUNCTIONS    
    
    def action(self):
        self.addAndDraw("test1","screen",20,20,400,400,"NW","red")
        self.addAndDraw("test2","graph",cWidth/2,cHeight/2,500,500,"C")
        self.addAndDraw("test3","screen",500,400,250,250,"E","blue")
    
    def addAndDraw(self,name,sType,x,y,cWidth,cHeight,factor,loc,color = "grey"):
        self.addScreen(name,sType,x,y,cWidth,cHeight,factor,loc,color)
        self.setScreenAbove(name)
        
    def addScreen(self,name,sType,x,y,cWidth,cHeight,factor,loc,color = "grey"):
        if (sType == "screen"):
            screen = Screen(name,self,x,y,cHeight,cWidth,self.height,self.width,factor,"grey",loc)
            self.screens[name] = screen
        if (sType == "graph"):
            screen = Graph(name,self,x,y,cWidth,cHeight,self.height,self.width,factor,loc)
            self.screens[name] = screen
            
    def setScreenAbove(self,name):
        print self.screens
        if name in self.screens:
            screen = self.screens[name]
            self.primaryScreen = screen
            self.drawScreens.append(screen)
            
    def removeScreen(self,name):
        if name in self.screens:
            for screen in self.drawScreens:
                if str(screen) == name:
                    pop(screen)
            del self.screens[name]
            
    def removeDrawScreen(self,name):
        for screen in self.drawScreens:
            if str(screen) == name:
                pop(screen)
    
    # DRAWING FUNCTIONS
    
    def drawBackGround(self,sType,cWidth,cHeight):
        if (sType == "graph"):
            screen = Screen("BG",0,0,cWidth,cHeight,self.height,self.width,1,"grey","NW")
        if (sType == "screen"):
            screen = Graph("BGraph",0,0,cWidth,cHeight,self.height,self.width,1,"NW")
     
        
class Screen(object):
    def __init__(self,name,parent,x,y,cHeight,cWidth,height,width,factor,color,loc):
        self.canvas = parent.canvas
        self.name = name
        self.parent = parent
        self.unitSize = parent.unitSize
        self.gcHeight = cHeight * factor
        self.gcWidth = cWidth * factor
        self.gWidth = int(width*factor)
        self.gHeight = int(height*factor)
        coords = self.processCoords(cWidth*factor,cHeight*factor,x,y,loc)
        self.x0,self.y0,self.x1,self.y1 = coords[0],coords[1],coords[2],coords[3]
        self.drawBlankScreen(self.x0,self.y0,self.x1,self.y1,color)
        
    def __str__(self):
        return self.name
        
    def draw(self):
        self.drawBlankScreen(self.x0,self.y0,self.x0,self.y0,self.color)
             
    def drawBlankScreen(self,x0,y0,x1,y1,color):
        c = self.canvas
        c.create_rectangle(x0,y0,x1,y1,fill = color)
               
    def processCoords(self,gcWidth,gcHeight,x,y,loc):
        x0 = 0
        y0 = 0
        x1 = 0
        y1 = 0
        horiz = False
        vertic = False
        if ("C"):
            x0 = x-gcWidth/2
            x1 = x+gcWidth/2
            y0 = y-gcHeight/2
            y1 = y+gcHeight/2
        if ("N" in loc):
            y0 = y
            y1 = y + gcHeight
            vertic = True
        elif ("S" in loc):    
            y0 = y - gcHeight
            y1 = y
            vertic = True
        if ("W" in loc):
            x0 = x
            x1 = x + gcWidth
            horiz = True
        elif ("E" in loc):
            x0 = x - gcWidth
            x1 = x
            vertic = True
            
        if (not(vertic)):
            y0 = y-gcHeight/2
            y1 = y+gcHeight/2
        if (not(horiz)):
            x0 = x-gcWidth/2
            x1 = x+gcWidth/2  
        return (x0,y0,x1,y1)
        
    
class Graph(Screen):
    def __init__(self,name,parent,x,y,cHeight,cWidth,height,width,factor,loc):
        super(Graph,self).__init__(name,parent,x,y,cHeight,cWidth,height,width,factor,"grey",loc)
        self.canvas = parent.canvas
        self.name = name
        self.parent = parent
        self.unitSize = parent.unitSize * factor
        self.gcHeight = cHeight * factor
        self.gcWidth = cWidth * factor
        self.gWidth = int(width*factor)
        self.gHeight = int(height*factor)
        coords = self.processCoords(cWidth*factor,cHeight*factor,x,y,loc)
        self.x0,self.y0,self.x1,self.y1 = coords[0],coords[1],coords[2],coords[3]
        self.drawBlankGraph(self.x0,self.y0,self.x1,self.y1)
        
    def drawBlankGraph(self,x0,y0,x1,y1):
        c = self.canvas
        unit = self.unitSize
        self.drawBlankScreen(x0,y0,x1,y1,"grey")
        xMid = x0 + (x1-x0)/2.
        yMid = y0 + (y1-y0)/2.
        c.create_line(xMid,y0,xMid,y1,width=2)
        c.create_line(x0,yMid,x1,yMid,width=2)
        
        for i in xrange(1,self.gHeight+1):
            cY = y0 + i*unit
            c.create_line(xMid-unit/4,cY,xMid+unit/4,cY,width = 1)
            
        for j in xrange(self.gWidth):
            cX = x0 + j*unit
            c.create_line(cX,yMid-unit/4,cX,yMid+unit/4,width = 1)
            
    def draw(self):
        self.drawBlankGraph(self.x0,self.y0,self.x1,self.y1)
    
        
        
app = CalculatorApp(800,40)
             
            
            
            