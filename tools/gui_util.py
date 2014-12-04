from util import *
from Tkinter import *

class CoordTransform:
    def __init__(self,cHeight,cWidth,xMin,xMax,yMin,yMax):
        self.yInt = cHeight / (yMax - yMin)
        self.xInt = cWidth / (xMax - xMin)
        self.cHeight = cHeight
        self.cWidth = cWidth
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax
        self.bounds = Rect(Point(xMin,yMax), Point(xMax,yMin))

    def MtoV(self,point):
        if (self.bounds.inBounds(point)):
            return Point((point.x - self.xMin) * self.xInt,
            			    self.cHeight - (point.y - self.yMin) * self.yInt)
        else:
            return None

    def scaleFactor(self):
        xScale = (self.cWidth / (self.xMax - self.xMin))
        yScale = (self.cHeight / (self.yMax - self.yMin))
        return (xScale + yScale)/2.

#define a simulation object that outputs states to a gui
class Simulation(object):
    
    def __init__(self, xmin, xmax, ymin, ymax):
			self.bounds = Rect(Point(xmin, ymax), Point(xmax, ymin))
		
    def step(self):
        return ("FINISHED", [])

class GUI(object): 
	def __init__(self, disable_high_gui, canvasWidth, canvasHeight, sim, delay): 
		self.root = Tk() 
		
		#initialize the game 
		self.cWidth = canvasWidth 
		self.cHeight = canvasHeight 
		self.sim = sim 
		self.game_bounds = sim.bounds
		self.disable_high_gui = disable_high_gui 
		self.CT = CoordTransform(canvasWidth, canvasHeight, sim.bounds.tl.x, sim.bounds.br.x,
														 sim.bounds.br.y, sim.bounds.tl.y)
		self.delay = delay
		
		#initialize canvas
		self.canvas = Canvas(self.root, width = canvasWidth, height = canvasHeight)
		self.canvas.pack()
		
	def run(self):
		#run
		self.timerFired(self.canvas)
		self.root.mainloop()
		
	def timerFired(self, canvas):
		output = self.sim.step()
		self.redrawAll(canvas, output)
		if (output[0] != "FINISHED"):
			canvas.after(self.delay, lambda c=canvas: self.timerFired(c))
		
	def redrawAll(self, canvas, state):
		canvas.delete(ALL)
		self.drawAxis(canvas, self.cWidth, self.cHeight, self.game_bounds, 1)
	
	def drawPoint(self, canvas, point, rad, color = "black"):
		gui_point = self.CT.MtoV(point)
		
		canvas.create_oval(gui_point.x - rad, gui_point.y - rad, gui_point.x + rad, gui_point.y + rad, fill = color, width = 0)
		
	def drawAxis(self,canvas, cWidth, cHeight, bounds, s_tick = 1):
		yInt = cHeight / (bounds.height())
		xInt = cWidth / (bounds.width())
		
		xMin = bounds.tl.x
		xMax = bounds.br.x
		yMin = bounds.br.y
		yMax = bounds.tl.y
		
		#vertical axis
		if (0.0 > xMin and 0.0 < xMax):
			xMid = xInt * (0.0 - xMin)
			yMid = cHeight - yInt * (0.0 - yMin)
			canvas.create_line(xMid,0,xMid, cHeight)
			start = yMid
			while (start > 0):
				canvas.create_line(xMid - s_tick, start, xMid + s_tick, start)
				start -= yInt
			start = yMid
			while (start < cHeight):
				canvas.create_line(xMid - s_tick, start, xMid + s_tick, start)
				start += yInt
				
		#horizontal axis
		if (0.0 > yMin and 0.0 < yMax):
			xMid = xInt * (0.0 - xMin)
			yMid = cHeight - yInt * (0.0 - yMin)
			canvas.create_line(0,yMid, cWidth, yMid)
			start = xMid
			while (start > 0):
				canvas.create_line(start, yMid - s_tick, start, yMid + s_tick)
				start -= xInt
			start = xMid
			while (start < cHeight):
				canvas.create_line(start, yMid - s_tick, start, yMid + s_tick)
				start += xInt
	