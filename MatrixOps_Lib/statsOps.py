#--------- STATISTICS OPERATIONS --------- #
# ---------- Vivek Krishnan ---------------#

# Basic Stats Ops

# MATRIX refers to a 2 dimensional list (rectangular)
# VECTOR refers to a 1 dimensional list
# NUMBER refers to type FLOAT or INT
# POLYNOMIAL refers to a vector such that [a,b,c,d...] represents a+bx+cx^2+dx^3...
# POINTLIST refers to a list of Cartesian coords, [(x1,y1),(x2,y2)...]


###########################################################
###################### INTERFACE ##########################
###########################################################




#######################################################
######################## USES #############################
###########################################################

import copy
import string

from utilityFuncs import *
from basicOps import *
from matrixSolver import *

###########################################################
###################### FUNCTIONS ##########################
###########################################################

def calcXYMeans(pointList):
    n = len(pointList)
    xAdd = 0.0
    yAdd = 0.0
    for i in xrange(n):
        xAdd += pointList[i][0]
        yAdd += pointList[i][1]
    xBar = xAdd / n
    yBar = yAdd / n
    return(xBar,yBar)

def calcStandardDev(pointList,xBar,yBar):
    n = (len(pointList))
    sX = 0.0
    sY = 0.0
    for i in xrange(n):
        sX += pow(pointList[i][0]-xBar,2)
        sY += pow(pointList[i][1]-yBar,2)
    return (sqrt(sX/n),sqrt(sY/n))

def calcCorrelation(pointList):
    means = calcXYMeans(pointList)
    xBar = means[0]
    yBar = means[1]
    n = len(pointList)
    sX = 0.0
    sY = 0.0
    sXsY = 0.0
    for i in xrange(n):
        sX += pow(pointList[i][0]-xBar,2)
        sY += pow(pointList[i][1]-yBar,2)
    sX = sqrt(sX)
    sY = sqrt(sY)
    for j in xrange(n):
        sXsY += ((pointList[i][0]-xBar)/sX) * ((pointList[i][1]-yBar)/sY)    
    return sXsY / (n-1)
 
def oneVarPopSD(numList):
    xBar = mean(numList)
    n = len(numList)
    sX = 0.0
    for i in xrange(n):
        sX += (numList[i] - xBar)
    sX /= n
    return sqrt(sX)
    
def oneVarSampSD(numList):
     xBar = mean(numList)
     n = len(numList)
     sX= 0.0
     for i in xrange(n):
         sX += pow(numList[i] - xBar,2)
     sX /= (n-1)
     return sqrt(sX)
    
def zScore(val,mean,sD):
    return (val-mean) / sD

    