from utilityFuncs import *
from basicOps import *
from matrixSolver import *
from statsOps import *
from Tkinter import *
import time
import random


#DRAWING FUNCTIONS


class StatsApp(object):
    def mousePressed(self, event): pass
    def keyPressed(self, event): pass
    
    def __init__(self,sideLength,unitSize):
        root = Tk()
        canvas = Canvas(root,width = sideLength,height = sideLength)
        self.root = root
        self.canvas = canvas
        self.cHeight = sideLength
        self.cWidth = sideLength
        self.unitSize = unitSize
        self.canvas.pack()
        self.width = sideLength/unitSize
        self.height = sideLength/unitSize
        self.step = 1 # determines how smooth curves are drawn (1 is best)
        self.pDim = 1 # dimensions of the radius of the points
        self.lDim = 4 # dimension of the length of the dashes
        self.polynomials = []
        self.pointList = []
        self.formulas = []
        self.zLevel = 0
        self.zStandard = 0
        self.zStep = 2
        self.bestFit = []
        self.lines = []
        self.statsInfo = False
        self.primaryScreen = "graph"
        self.redrawAllWrapper()
    
    def init(self):
        self.step = 1 # determines how smooth curves are drawn (1 is best)
        self.pDim = 2 # dimensions of the radius of the points
        self.lDim = 4 # dimension of the length of the dashes
        self.polynomials = []
        self.points = []
        self.formulas = []
        self.bestFit = []
        self.zLevel = 0
        self.primaryScreen = "graph"
        self.redrawAllWrapper()
    
    def redrawAllWrapper(self):
        self.canvas.delete(ALL)
        self.redrawAll()
    
    def mousePressedWrapper(self,event):
        self.mousePressed(event)
        #self.redrawAllWrapper()
        
    def keyPressedWrapper(self,event):
        self.keyPressed(event)
        self.redrawAllWrapper()
    
    def redrawAll(self):
        if self.primaryScreen == "graph":
            self.drawBlankGraph(self.cHeight,self.cWidth,self.height,self.width)
        else:
            self.drawBlankScreen(self.cHeight,self.cWidth,"grey",1)
        self.drawPoints(self.pointList)
        if (self.primaryScreen == "graph"):
            self.drawPolynomials(self.polynomials)
        if (self.primaryScreen == "graph"):
            self.drawFormulas(self.formulas)
        [self.drawPolynomial(poly,"green") for poly in self.bestFit]
        [self.drawEquation(self.canvas,self.cHeight,self.cWidth,poly) for poly in self.bestFit]
        if (self.primaryScreen == "stats"):
            self.drawStatsInfo(self.cHeight,self.cWidth,self.height,self.width)
        if (len(self.polynomials) == 1 and len(self.formulas) == 0 and self.primaryScreen == "graph"):
            self.drawEquation(self.canvas,self.cHeight,self.cWidth,self.polynomials[0])
        if self.primaryScreen == "addScreen":
            self.drawAddScreen(self.cWidth,self.cHeight)
        
        
    def mousePressed(self,event):
        print event.x,event.y
        
    def keyPressed(self,event):
        print event.keysym
        if (event.keysym == "q" and self.primaryScreen == "graph"):
            self.zoomIn()
            self.redrawAllWrapper()
        elif(event.keysym == "w" and self.primaryScreen == "graph"):
            self.zoomOut()
            self.redrawAllWrapper()
        elif(event.keysym == "a"):
            self.primaryScreen = "addScreen"
        #elif(event.keysym == "s" and len(self.pointList) >= 2):
        #    if self.primaryScreen == "stats":
        #        self.primaryScreen = "graph"
        #    else:
        #        self.primaryScreen = "stats"
        #        self.zoomStandard()
        #        self.zoomIn()
        #        self.redrawAllWrapper()
        #elif(event.keysym == "b" and len(self.pointList) >= 2):
        #     if len(self.bestFit) == 0:
        #         self.bestFit.append(nthDegreeRegression(self.pointList,1))
        #     else:
        #         self.bestFit = []
                   
    def run(self):
        self.root.bind("<Button-1>",self.mousePressedWrapper)
        self.root.bind("<Key>",self.keyPressedWrapper)
        self.root.mainloop()    
        
    def zoomIn(self):
        if (self.height <= 5 or self.width <= 5):
            self.height = 5
            self.width = 5
        elif(self.zLevel < 3):
            self.zLevel += 1
            self.unitSize *= self.zStep
            self.height /= self.zStep
            self.width /= self.zStep
        self.redrawAllWrapper()
        
    def zoomOut(self):
        if (self.height >= 2000 or self.width >= 2000):
            self.height = 2000
            self.width = 2000
        elif(self.zLevel > -3):
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
    
    def drawTitle(self,cHeight,cWidth,title):
        c = self.canvas
        c.create_text(cWidth/2,5,text = title, anchor = N)
    
    def drawBlankScreen(self,cHeight,cWidth,color = "white",factor = 1):
        c = self.canvas
        name = self.primaryScreen
        c.create_rectangle(cWidth*(.5-factor/2.),cHeight*(.5-factor/2.),
                           cWidth*(.5+factor/2.),cHeight*(.5+factor/2.),fill = color)
        self.drawTitle(cHeight,cWidth,name)
        
    def drawContentScreen(self,lB,tB,rB,bB,color):
        pass
        
    def drawBlankGraph(self,cHeight,cWidth,height,width,factor = 1):
        c = self.canvas
        gcHeight = cHeight * factor
        gcWidth = cWidth * factor
        gWidth = int(width*factor)
        gHeight = int(height*factor)
        cMid = (cHeight/2,cWidth/2)
        c.create_rectangle(cMid[0]-gcWidth/2,cMid[1]-gcHeight/2,
                           cMid[0]+gcWidth/2,cMid[1]+gcHeight/2,fill="grey")
        c.create_line(cMid[0]-gcWidth/2,cMid[1],cMid[0]+gcWidth/2,cMid[1],fill="black",width=2)
        c.create_line(cMid[0],cMid[1]-gcHeight/2,cMid[0],cMid[1]+gcHeight/2,fill="black",width=2)
        for j in xrange(gWidth):
            center = cMid[0]-gcWidth/2 + j*self.unitSize
            c.create_line(center,cHeight/2+self.lDim,center,cHeight/2-self.lDim)
        # create the dashes on the vertical axis
        for k in xrange(height):    
            center = cMid[1]-gcHeight/2 + k*self.unitSize
            c.create_line(cWidth/2+self.lDim,center,cWidth/2-self.lDim,center)
    
    def drawAddScreen(self,cHeight,cWidth):
        maxSize = cWidth * .9
        
        self.drawBlankScreen(cHeight,cWidth,"white", maxSize,"white")
        self.drawContentScreen()
        self.drawContent()
    
    def addPoint(self,point):
        #point is an (x,y) tuple
        if (point == None or point[1] == None or point[0] == None):
            return
        self.pointList.append(point)
        self.redrawAllWrapper()
    
    def drawPoints(self,pointList):
        for point in pointList:
            if (point[1] == None or point[0] == None):
                pointList.remove(point)
                continue
            self.drawPoint(point[0],point[1])
    
    def drawPoint(self,x,y,primary = "black", secondary = "white"):
        c = self.canvas
        cX = x*self.unitSize + self.cWidth/2
        cY = self.cHeight/2 - y*self.unitSize
        c.create_oval(cX-self.pDim,cY-self.pDim,
                      cX+self.pDim,cY+self.pDim,fill = primary)
        c.create_oval(cX-self.pDim/2,cY-self.pDim/2,
                      cX+self.pDim/2,cY+self.pDim/2,fill = secondary)   
    
    def addPolynomial(self,poly):
        self.polynomials.append(poly)
        self.redrawAllWrapper()
    
    def drawPolynomials(self,polyList):
        colorList = ["red","blue","green","pink","orange","yellow","black"]
        i = 0
        for poly in polyList:
            color = colorList[i]
            self.drawPolynomial(poly,color)
            i += 1
                      
    def drawPolynomial(self,poly,color = "black"):
        c = self.canvas
        prevPoint = (-self.width/2,solveOutPolynom(poly,-self.width/2))
        for xPix in xrange(0,self.cWidth+1,self.step):
            x = (xPix-self.cWidth/2)/float(self.unitSize)
            y = solveOutPolynom(poly,x)
            x0 = prevPoint[0] * self.unitSize + self.cWidth/2
            y0 = self.cHeight/2 - prevPoint[1] * self.unitSize
            x1 = x * self.unitSize + self.cWidth/2
            y1 = self.cHeight/2 - y * self.unitSize
            c.create_line(x0,y0,x1,y1,width=2,fill=color)
            prevPoint = (x,y)
    
    def addFormula(self,formula):
        self.formulas.append(formula)
        self.redrawAllWrapper()
        
    def drawFormulas(self,formulas):
        for formula in formulas:
            self.drawFormula(formula)
    
    def drawFormula(self,f,color = "blue"):
        c = self.canvas
        prevPoint = (-self.width/2,f(-self.width/2))
        for xPix in xrange(0,self.cWidth+1,self.step):
            x = (xPix-self.cWidth/2)/float(self.unitSize)
            try:
                y = f(x)
            except:
                y = None
            if y == None:
                prevPoint= (x,None)
                continue
            if (y != None and prevPoint[1] == None):
                prevPoint = (x,y)
                continue
            if (x>0):
                print y
            x0 = prevPoint[0] * self.unitSize + self.cWidth/2
            y0 = self.cHeight/2 - prevPoint[1] * self.unitSize
            x1 = x * self.unitSize + self.cWidth/2
            y1 = self.cHeight/2 - y * self.unitSize
            c.create_line(x0,y0,x1,y1,width=2,fill=color)
            prevPoint = (x,y)
            
    def drawEquation(self,canvas,cHeight,cWidth,poly):
        polynomial = ""
        height = cHeight/50
        for i in xrange(len(poly)):
            if (i == 0):
                polynomial += " %.3f  " %(poly[0])
            else:
                polynomial += " +   %.3f x^%d " %(poly[i],i)
        width = len(polynomial) * (cWidth/100.)
        canvas.create_rectangle(cWidth-width*2/3.,0,cWidth,height,fill="white")
        ptSize = int(cWidth/100./.75)
        canvas.create_text(cWidth-width/3,height/2+2,text=polynomial,font = ("Helvetica",ptSize))

    def drawStatsInfo(self,cHeight,cWidth,height,width):
        c= self.canvas
        c.create_text(cWidth/2,cHeight/40,text = "Stats")
        
        
    def drawZGraph(self,cHeight,cWidth,height,width,numList,color):
        c = self.canvas
        sY = oneVarSampSD(numList)
        xBar = mean(numList)
        term = (1/(sY*sqrt(2*PI)))
        term2 = 2*pow(sY,2)
        f = lambda x: term * exponential_function(-pow((x-xBar),2)/term2)
    
        
    def integrate(self,f1,f2,lB,rB):
        if (lB > rB):
            lB,rB = rB,lB
        c = self.canvas
        lowB = int(lB*self.unitSize+self.cWidth/2)
        highB = int(rB*self.unitSize+self.cWidth/2)
        integral = 0.0
        for i in xrange(lowB,highB+self.step,self.step):
            x = (i - self.cWidth/2.)/self.unitSize
            y0 = self.cHeight/2 - f1(x) * self.unitSize
            y1 = self.cHeight/2 - f2(x) * self.unitSize 
            integral += ((y1-y0) * self.step)/(self.unitSize**2)
        return integral
        

def initGraph(canvas,cWidth,cHeight,pList,unit,allLines,default,showRegress):
    maxDegree = 7
    #draw Lines
    if (len(pList) <= 2):
        poly = nthDegreeRegression(pointList,2)
        drawLine(canvas,cHeight,cWidth,height,width,poly,step,unit)
    else:
        if (allLines):
            colors = ["red","yellow","orange","green","blue","purple","pink","white","black"]
            for i in xrange(0,min(len(pList),maxDegree)):
                poly = nthDegreeRegression(pointList,i)
                drawLine(canvas,cHeight,cWidth,height,width,poly,step,unit,colors[i])
        else:
            poly = nthDegreeRegression(pointList,default)
            drawLine(canvas,cHeight,cWidth,height,width,poly,step,unit)
    #create all the points
   
    #draw features
    if (allLines):
        drawKey(canvas,cHeight,cWidth,pList,maxDegree)
    if(not(allLines)):
        drawEquation(canvas,cHeight,cWidth,poly)
    #if(showRegress or not(allLines)):
    #    drawRegress(canvas,pList)
    drawZoomButton(canvas,cHeight,cWidth)

def drawEquation(canvas,cHeight,cWidth,poly):
    polynomial = ""
    height = cHeight/50
    for i in xrange(len(poly)):
        if (i == 0):
            polynomial += " %.3f  " %(poly[0])
        else:
            polynomial += " +   %.3f x^%d " %(poly[i],i)
    width = len(polynomial) * (cWidth/100.)
    canvas.create_rectangle(cWidth-width*2/3.,0,cWidth,height,fill="white")
    canvas.create_text(cWidth-width/3,height/2+2,text=polynomial)

def drawKey(canvas,cHeight,cWidth,pList,maxDegree):
    height = cHeight/50
    width = cWidth/10
    colors = ["red","yellow","orange","green","blue","purple","pink","white","black"]
    drawHeader(canvas,height,width)
    cur = height + 5
    for i in xrange(min(len(pList)+1,maxDegree)):
        drawDegree(canvas,height,width,cur,colors[i],i)
        cur += height
        
def drawHeader(canvas,height,width):
    canvas.create_rectangle(2,5,width,height+5,fill="white",width="2",outline = "black")
    canvas.create_text(width/2,height/2+5,text = "KEY")

def drawDegree(canvas,height,width,cur,color,drg):
    canvas.create_rectangle(2,cur,width,cur+height,fill="white",width="1")
    sqSize = height/4
    sqOff = width/10
    canvas.create_rectangle(sqOff,cur+height/2-sqSize,sqOff+2*sqSize,cur+height/2+sqSize,
                            width="1",fill=color)
    textDegree = "Degree %d" %(drg)
    ftSizePix = 2*sqSize + sqOff
    ftSize = int(round(ftSizePix*.75))
    canvas.create_text(width/2+sqOff,cur + height/2 + sqSize/2,text = textDegree,
                        font=("Helvetica",ftSize))

def drawLine(canvas,cHeight,cWidth,height,width,poly,step,unit,color = "blue"):
    prevPoint = (-width/2,solveOutPolynom(poly,-width/2))
    for xPix in xrange(0,cWidth+1,step):
        x = (xPix-cWidth/2)/float(unit)
        y = solveOutPolynom(poly,x)
        x0 = prevPoint[0] * unit + cWidth/2
        y0 = cHeight/2 - prevPoint[1] * unit
        x1 = x * unit + cWidth/2
        y1 = cHeight/2 - y * unit
        canvas.create_line(x0,y0,x1,y1,width=2,fill=color)
        prevPoint = (x,y)
        
def drawZoomButton(canvas,cWidth,cHeight):
      height = cHeight/25
      width = cWidth/10
      canvas.create_rectangle(0,cHeight-height,width,cHeight,fill="white")
      canvas.create_rectangle(width,cHeight-height,2*width,cHeight,fill="white")
      canvas.create_text(width/2,cHeight-height/2,text="Zoom In")
      canvas.create_text(width/2+width,cHeight-height/2,text="Zoom Out")
        
def run(pointList, allLines,showRegress,default = 2):
    root = Tk()
    width = 840
    height = 840
    unitSize = 40
    c=Canvas(root,width=width,height=height)
    c.pack()
    initGraph(c,width,height,pointList,unitSize,allLines,default,showRegress)
    mainloop()

def createNthRandomMatrix(n):
    matrix = make2dList(n,n)
    for row in xrange(n):
        for col in xrange(n):
            matrix[row][col] = random.random() * random.randint(0,100)
    return matrix

def createTimeList(numPoints,increment,n):
    times = []
    matrix = []
    for i in xrange(0,numPoints):    
        matrix = createNthRandomMatrix(n)
        t2 = time.time()
        temp = (matrixInverse(matrix))    
        t3 = time.time()
        times.append((n,t3-t2))
        n+=increment
        print times
    return times

tL = [(50, 0.12426400184631348), (100, 0.9021899700164795), (150, 2.9514808654785156), (200, 6.986707925796509), (250, 13.867085933685303), (300, 24.88462781906128), (350, 41.0455219745636), (400, 65.0557119846344), (450, 92.33589005470276), (500, 129.06875014305115)]

def makeRandPoints(numPoints,xMin,xMax,yMin,yMax):
    pList = []
    taken = set()
    for i in xrange(numPoints):
        x = xMin + (xMax-xMin)*random.random()
        y = yMin + (yMax-yMin)*random.random()
        pList.append((x,y))
    return pList

def series(x,depth = 0,alt = 1):
    if x <= 0 or depth > 20: 
        return
    else:
        temp = series(x,depth+1,alt*-1)
        if temp == None:    
            return alt* 1./x 
        else:
            return alt*  1./x + temp

my_fun = lambda x: function(polynom,x)

[statsApp.addPoint((x,y)) for (x,y) in pointList]
statsApp.run()