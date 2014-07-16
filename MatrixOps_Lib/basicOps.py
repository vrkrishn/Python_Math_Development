#---------BASIC MATRIX OPERATION --------- #
# ---------- Vivek Krishnan ---------------#

# Basic matrix operations that are essential for more complicated operations

# MATRIX refers to a 2 dimensional list (rectangular)
# VECTOR refers to a 1 dimensional list
# NUMBER refers to type FLOAT or INT


###########################################################
###################### INTERFACE ##########################
###########################################################

# BASIC OPS

#def isZeroVector(v):
    #vector v
    #returns whether all elements of v are zero

#def findLargestRow(a):
    #matrix a
    #utility for ragged list in order to rectangularize them
    #returns a tuple representing the largest row number and its length

#def rectangularize(a):
    #matrix a
    #returns a matrix that is rectangular, even if input it ragged. Empty spots are filled in with 0.0

#def augmentedMatrix(matrix,solution):
    #matrix matrix, vector solution
    #returns a matrix that contains the original matrix with the solution matrix added as the last column
    
#def separateMatrixFromAugmented(matrix,colStart,colEnd):
    #matrix matrix, number colStart, number colEnd
    #REQUIRES(0 <= colEnd and colEnd < len(aMatrix[0]) and 0<=colStart and colStart < colEnd)
    #returns a subMatrix of matrix stretching from column  colStart to column colEnd

#def norm(vector):
    #vector vector
    #returns the magnitude of the vector

#def normalize(vector):
    #vector vector
    #returns a new vector that represents the normalized original vector with magnitude of 1

#def normalize2d(matrix):
    #matrix matrix
    #applies the normalize operation over all columns of the matrix
    
#def extractColumn(a,col):
    #matrix a, number col
    #REQUIRES (0 <= col < len(a[0]))
    #returns vector that consists of entries from column col of matrix a

# BASIC MATRIX AND VECTOR OPERATIONS

#def matrixAdd(matrix1,matrix2):
    # matrix matrix1, matrix matrix2
    # REQUIRES (dimensions(matrix1) == dimensions(matrix2))
    #returns a new matrix whose ith,jth entry is the sum of the ith,jth entries of
    #matrix 1 and matrix 2

#def matrixSub(matrix1,matrix2):
    # matrix matrix1, matrix matrix2
    # REQUIRES (dimensions(matrix1) == dimensions(matrix2))
    #returns a new matrix whose ith,jth entry is the result of subtracting the
    #ith,jth entry of matrix 2 from the ith,jth entry of matrix 1
    
#def vectorAdd(v1,v2):
    #  vector v1, vector v2
    # REQUIRES (length(v1) == length(v2))
    #returns a new vector whose ith entry is the sum of the ith entries of
    #vector 1 and vector 2

#def vectorSub(v1,v2):
    # vector v1, vector v2
    # REQUIRES (length(v1) == length(v2))
    #returns a new vector whose ith entry is the result of subtraction the
    #ith entry of v2 from the ith entry of v1
    
#def vectorScalar(v1,c):
    #  vector v1, number c
    # returns a vector that represents entries of v1 multiplied by a constant c
    
#def dotProduct(a,b):
    # vector a, vector b
    # returns a number that represents the dot product of a and b
    
#def transpose(a):
    #matrix a
    #returns a new matrix such that the ith,jth entry of a is the jth,ith entry of
    # the result
    
#def scalarMultiply(matrix,c):
    #matrix matrix, number c
    #returns a new matrix such that the ith,jth element of the result is the ith,jth
    # element of the matrix multiplied by constant c
  
# GAUSSIAN ELIMINATION
    
#def rowExchange(a,r1,r2):
    #matrix a, number r1, number r2
    #REQUIRES (0 <= r1 < len(a) and 0 <= r2 < len(a))
    #returns a new matrix identical to the original matrix save that row r1 and row r2
    # are switched
    
#def colExchange(a,c1,c2):
    #matrix a, number c1, number c2
    #REQUIRES (0 <= c1 < len(a[0]) and 0 <= c2 < len(a[0]))
    #returns a new matrix identical to the original matrix save that col c1 and col c2
    # are switched
    
#def multiplyRow(a,r,m):
    #matrix a, number r, number m
    #REQUIRES (0 <= r < len(a) and m!= 0)
    #returns a matrix identical to a except that the rth row entries have been
    #multiplied by constant m
    
#def addMultipleOfRow(a,r1,r2,m):
    #matrix a, number r1, number r2, number m2
    #REQUIRES (0 <= r1 < len(a) and 0 <= r2 < len(a))
    #returns a matrix identical to a except that the r1th row entries have been
    #multiplied by the r2th row entries of the same column
    
#def eliminateVariable(a,r1,r2,col):
    #matrix a, number r1, number r2, number col
    #REQUIRES (0 <= r1 < len(a) and 0 <= r2 < len(a) and 0 <= col < len(a[0]))
    #returns a matrix that is identical to a save that a certain multiple of r2 has been added to r1 to make the
    #r1th,col entry 0.0


###########################################################
######################## USES #############################
###########################################################

from utilityFuncs import *

###########################################################
###################### FUNCTIONS ##########################
###########################################################

def matrixAdd(matrix1,matrix2):
    #adds 2 to 1
    assert(len(matrix1) == len(matrix2) and len(matrix1[0])==len(matrix2[0]))
    result = make2dList(len(matrix1),len(matrix1[0]))
    for i in xrange(len(matrix1)):
        for j in xrange(len(matrix1[0])):
            result[i][j] = matrix1[i][j] + matrix2[i][j]
    return result
    
def matrixSub(matrix1,matrix2):
    #subtracts 2 from 1
    return matrixAdd(matrix1,scalarMultiply(matrix2,-1))
    
def vectorAdd(v1,v2):
    assert(len(v1)==len(v2))
    return [v1[i]+v2[i] for i in xrange(len(v1))]
    
def vectorSub(v1,v2):
    assert(len(v1)==len(v2))
    return [v1[i]-v2[i] for i in xrange(len(v1))]
    
def vectorScalar(v1,c):
    assert(type(c) == float or type(c) == int)
    return [v1[i] * c for i in xrange(len(v1))]    
    
def dotProduct(a,b):
    assert(len(a) == len(b))
    result = 0
    length = min(len(a),len(b))
    for i in xrange(length):
        result += a[i]*b[i]
    return result 
           
def extractColumn(a,col):
    # extract a column from a matrix
    assert(col >= 0 and col < len(a[0]))
    result = []
    for i in xrange(len(a)):
        result.append(a[i][col])
    return result    
    
def transpose(a):
    #transpose a matrix
    row = len(a)
    col = len(a[0])
    result = make2dList(col,row)
    for i in xrange(row):
        for j in xrange(col):
            temp = a[i][j]
            result[j][i]=temp
    return result
 
def scalarMultiply(matrix,c):
    result = make2dList(len(matrix),len(matrix[0]))
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
             result[i][j] = matrix[i][j] * c
    return result
    
def rowExchange(a,r1,r2):
    #exchanges 2 rows
    assert(0 <= r1 < len(a) and 0 <= r2 < len(a))
    result = a
    (result[r1],result[r2]) = (result[r2], result[r1])
    return result
 
def colExchange(a,c1,c2):
    #exchange 2 columns
    assert(0 <= c1 < len(a[0]) and 0 <= c2 < len(a[0]))
    result = a
    for i in xrange(len(a)):
        (result[i][c1],result[i][c2]) = (result[i][c2],result[c1])
    return result
        
def multiplyRow(a,r,m):
    assert(0 <= r < len(a) and m != 0)
    #multiple r1 by a non-zero value
    result = a
    for i in xrange(len(a[0])):
        result[r][i] = result[r][i]*m
        if (result[r][i] == -0.0):
            result[r][i] = 0.0
    return result
    
def addMultipleOfRow(a,r1,r2,m):
    #add a multiple of r1 to r2
    assert(0 <= r1 < len(a) and 0 <= r2 < len(a))
    result = a
    for i in xrange(len(a[0])):
        result[r2][i] = result[r2][i] + m*result[r1][i]
    return result
    
def eliminateVariable(a,r1,r2,col):
    #eliminate a variable at specified col from r2 through gaussian elimination
    assert((0 <= r1 < len(a) and 0 <= r2 < len(a) and 0 <= col < len(a[0])))
    if (a[r1][col] != 0):
        factor = float(a[r2][col])/float(a[r1][col])
        result = addMultipleOfRow(a,r1,r2,-1*factor)
        return result
    else:
        return a

def isZeroVector(v):
    for elem in v:
        if not(almostEquals(elem,0.0)):
            return False
    return True
    
def findLargestRow(a):
    largestCol = 0
    length = 0
    tLength = 0
    for x in xrange(1,len(a)):
        if type(a[0])!=list:
            tLength = 1
        else:
            tLength = len(a[0])
        if tLength > length:
            length = tLength
            largestRow = x
    return (largestRow,length)
    
def rectangularize(a):
    data = findLargestRow(a)
    result = make2dList(len(a),data[1])
    for i in xrange(len(result)):
        for j in xrange(len(result[0])):
            if (j >= len(a[i]) or type(a[i]) != list):
                result[i][j] = 0.0
            else:
                result[i][j] = a[i][j]
    return result
        
def augmentedMatrix(matrix,solution):
    assert(len(matrix) == len(solution))
    cols = len(matrix[0])
    augmented = make2dList(len(matrix),cols+1)
    for i in xrange(len(matrix)):
        for j in xrange(cols+1):
            if ( j >= cols ):
                augmented[i][j] = solution [i]
            else:
                augmented[i][j] = matrix[i][j]
    return augmented

def separateMatrixFromAugmented(aMatrix,colStart,colEnd):
    assert(0 <= colEnd and colEnd < len(aMatrix[0]) and 0<=colStart and colStart < colEnd)
    matrix = make2dList(len(aMatrix),colEnd-colStart)
    for i in xrange(len(matrix)):
        for j in xrange(colStart,colEnd):  
            matrix[i][j] = aMatrix[i][j]
    return matrix

def norm(vector): 
     sum = 0
     for entry in vector:
         sum += (entry) * (entry)
     return sqrt(sum)

def normalize(vector):
     factor = 1/norm(vector)
     new = copy.deepcopy(vector)
     for i in xrange(len(new)):
         new[i]*=factor
     return new
         
def normalize2d(matrix):
    result = make2dList(len(matrix),len(matrix[0]))
    for i in xrange(len(matrix[0])):
        vector = normalize(extractColumn(matrix,i))
        for j in xrange(len(vector)):
            result[j][i] = vector[j]
    return result

###################################################################

# TEST CODE STARTS HERE




