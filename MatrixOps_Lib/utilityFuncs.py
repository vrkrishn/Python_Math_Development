#--------- UTILITY FUNCTIONS --------- #
# ---------- Vivek Krishnan ---------------#

# Basic utility functions for use in further documents

# MATRIX refers to a 2 dimensional list (rectangular)
# VECTOR refers to a 1 dimensional list
# NUMBER refers to type FLOAT or INT
# POLYNOMIAL refers to a vector such that [a,b,c,d...] represents a+bx+cx^2+dx^3...


###########################################################
###################### INTERFACE ##########################
###########################################################

# UTILITY

#def countDigits(n):
    #int n
    #returns the number of digits in n

#def almostEquals(n1,n2):
    #number n1, number n2
    #checks for float equality (because floating point numbers have error)

#def vecTo2d(v1):
    #vector v1
    #return a matrix with 1 column and entries matching vector v1

# DISPLAY 

#def displaySolution(x,y):
    # vector x , vector y
    #REQUIRES(len(x)==len(y))
    # prints out each element of x + the corresponding element of y
    
#def display2dList(a):
    #matrix a
    #displays a 2dList with each entry rounded to 3 decimal places
    
#def displayPolynomial(polynomial):
    #displays a polynomial as an expression such that [a,b,c,d...] prints out a+bx+cx^2+dx^3...
    
# MATH
    
#def pow(x,y):
    # number a, number x
    # returns (a)^x
    
#def ln(x):
    #number x
    #returns a Taylor approximation of ln(x)

#def mean(a):
    # vector a
    # return the mean of the elements of a

# def gcd(x,y):
    # int a, int y
    # returns the greatest common factor of x and y

#def sqrt(x):
    #number x
    #returns the sqrt of x calculated as sqrt(x) = e^(0.5 * ln(x))
    
#def fact(n):
    #number n
    #returns factorial of n, n!
    
#def exponential_function(x):
    #number x
    #returns a Taylor approximation of e^x
  
# MATRIX CREATION     

#def make2dList(row,col):
    #number row, number col
    # returns a matrix with row rows and col cols, with 0.0 at each entry

#def makeIdentity(row,col):
    #number row, number col
    #returns a make2dList result except that entries such that row==col have
    # a value of 1.0 instead of 0.0 

#SPECIAL
    
#def solveOutPolynom(polynom,x):
    #polynomial polynom, number x
    #given a polynomial p, returns p(x)    

###########################################################
######################## USES #############################
###########################################################

import copy
import string


###########################################################
###################### GLOBALS ############################
###########################################################

PI = 3.14159265359
PHI = 1.618033988749
const_E = 2.71828182846

###########################################################
###################### FUNCTIONS ##########################
###########################################################


def displaySolution(x,y):
    assert(len(x)==len(y))
    for i in xrange(len(y)):
        print (x[i]), " + ", (y[i])

def pow(a,x):
    result = 1
    for i in xrange(x):
        result *= a
    return result

def fact(n):
    if (n == None):
        return None
    if (n <= 0):
        return 1
    else:
        return n*fact(n-1)
    
def almostEquals(n1,n2,epsilon=.0000001):
    return (abs(n1-n2) < epsilon)

def exponential_function(x,depth = 0,maxDepth = 50,test = 0):
    #e^x
    if (x < -15):
        return (0.0)
    if (depth > maxDepth):
        return 0
    else:
        return ((pow(x,depth))/float(fact(depth))) + exponential_function(x,depth+1)    

def countDigits(n):
    if (n == None):
        return 0
    assert(type(n)==int)
    i = 9
    count = 1
    while(i<=n):
        count+=1
        i*=10
    return count

def ln_mcLaurin(x,depth = 1, maxDepth = 20):
    if (depth > maxDepth):
        return 0
    else:
        return (1/float(depth)) * pow((x-1)/float(x+1),depth) + ln_mcLaurin(x,depth+2)  
    
def ln(x):
    if (x < 0):
        return None
    if (x == 0):
        return -10000
    assert(x > 0 )
    return 2*ln_mcLaurin(x)
    
def sin(x,alt = 1,depth = 0):
    x = x%(2*PI)
    if x == None:
        return None
    if (depth == 25):
        return 0
    else:
        return alt*(pow(x,2*depth+1))/float(fact(2*depth+1)) + sin(x,alt*-1,depth+1)

def cos(x,alt = 1, depth = 0): 
    x = x%(2*PI)   
    if x == None:
        return None
    if (depth == 25):
        return 0
    else:
        return alt*(pow(x,2*depth))/float(fact(2*depth)) + cos(x,alt*-1,depth+1)

def tan(x):
    if x == None:
        return None
    return sin(x)/cos(x)

def sqrt_series(x):
    return exponential_function((0.5)*ln(x))

def sqrt(x):
    if x == None:
        return None
    return sqrt_series(x)
 
def gcd(x,y,factor = 1):
    assert(type(x) == int and type(y) == int)
    maxi,mini = max(abs(x),(abs(y))),min(abs(x),(abs(y)))
    if (mini == 0):
        return maxi
    else:
        return gcd(mini,maxi%mini) 

def mean(a):
    return sum(a)/float(len(a))
   
def display2dList(a):
    if (type(a) == list):
        if a==None:
            return
        for row in a:
            row = [round(elem*10**3)/float(10**3) for elem in row]
            print row
    elif (len(a) == 2):
        displaySolution(a[0],a[1])

def displayPolynomial(inp):
    #input is the output from nthDegreeRegression
    polynomial = ""
    for i in xrange(len(inp)):
        if (i == 0):
            polynomial += " %.3f  " %(inp[0])
        else:
            polynomial += " +   %.3f x^%d " %(inp[i],i)
    print polynomial

def make2dList(row,col):
    return [ [0.0]*col for i in xrange(row)]
    
def makeIdentity(row,col):
    M = make2dList(row,col)
    for i in xrange(row):
        for j in xrange(col):
            if (i == j):
                M[i][j] = 1.0
    return M    

def vecTo2d(v1):
    result = make2dList(len(v1),1)
    for i in xrange(len(v1)):
        result[i][0] = v1[i]
    return result

def solveOutPolynom(polynom,x):
    result = 0
    for i in xrange(len(polynom)):
        result += polynom[i] * (x ** i)
    return result


# TEST CODE STARTS HERE