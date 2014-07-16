#--------- MATRIX SOLVER --------- #
# ---------- Vivek Krishnan ---------------#

# Complex Matrix Operations

# MATRIX refers to a 2 dimensional list (rectangular)
# VECTOR refers to a 1 dimensional list
# NUMBER refers to type FLOAT or INT
# POLYNOMIAL refers to a vector such that [a,b,c,d...] represents a+bx+cx^2+dx^3...
# POINTLIST refers to a list of Cartesian coords, [(x1,y1),(x2,y2)...]


###########################################################
###################### INTERFACE ##########################
###########################################################

# SOLVING SYSTEMS OF EQUATIONS
 
# def reducedEchelonForm(matrix):
    #matrix matrix
    # returns a matrix such that the first non-zero element in each row has to be a pivot
    # and all pivot columns are filled with zeroes, except for the pivot
    
# def matrixMultiply(a,b)
    #matrix a, matrix b
    #REQUIRES(0 <= colEnd and colEnd < len(aMatrix[0]) and 0<=colStart and colStart < colEnd)
    #does a matrix multiply operation and returns a matrix representing a x b
    
# def LU_FACTORIZATION(matrix):
    # matrix matrix
    # returns the LU factorization of matrix in a tuple as (L,U)
    
# def solveMatrixSystem(A,b):
    # matrix A, vector b
    # given a matrixSystem Ax = b, returns a value for x as a tuple (Particular Solution, Special Solution)
    
# FOUR FUNDAMENTAL SUBSPACES

# def columnSpace(M):
    #matrix M
    #returns the column space of M

# def rowSpace(M):
    #matrix M
    #returns the row space of M

# def nullSpace(M):
    #matrix M
    #returns the null space of M

# def leftNullSpace(M):
    #matrix M
    #returns the left null space of M

# INVERSE BY GAUSS-JORDAN    
    
# def matrixInverse(matrix):
    # matrix matrix
    # REQUIRES(isInvertable(matrix)) -- the matrix must have linearly independant columns
    # returns the inverse of the matrix
    
# ORTHOGONALITY

# def projectionMatrix(A):
    # matrix A
    # returns a matrix P such that given a matrix M, P x M will be in the column space of A
    
# def projection(a,b):
    # matrix a, matrix b
    # returns the projection of a onto b
    
# def QR_Factorization(matrix):
    # matrix matrix
    # returns the QR factorization of matrix in a tuple as (Q,R)
    
# DETERMINANTS    
    
# def det(matrix):
    # matrix matrix
    # returns the determinant of the matrix by coFactor expansion
    
#def detFromCoFactorMatrix(matrix,coFactor):
    # matrix matrix, matrix cofactor
    # since cofactor matrix is known, saves computation by finding det from existing coFactor Matrix
    
#def coFactorMatrix(matrix):
    # matrix matrix
    # generates a coFactor matrix for matrix
    
#def coFactorInverse(matrix)
    # matrix matrix
    # REQUIRES(isInvertable(matrix)) -- the matrix must have linearly independant columns
    # returns the inverse of matrix calculated by A-1 = transpose(C)/det(A)
    
# POLYNOMIAL OPERATIONS

# def nthDegreeRegression(pointList,drg):
    #pointList pointList, number drg
    #returns a polynomial of degree drg that best fits the data points
    
# def polynomDerive(polynomial)
    # polynomial polynomial
    # returns a polynomial representing the derivative of the input

# def polynomIntegrate(polynomial)
    # polynomial polynomial
    # returns a polynomial representing the integral of the input

#######################################################
######################## USES #############################
###########################################################

import copy
import string

from utilityFuncs import *
from basicOps import *

###########################################################
###################### FUNCTIONS ##########################

#Complex Basic Matrix Operations

def reducedEchelonForm(matrix):
    augmented = LU_Factorization(matrix)[1]
    #reduce all the pivots to 1
    for i in xrange(len(matrix)):
        index = 0
        while (index < len(augmented[i]) and almostEquals(augmented[i][index],0.0) ):
            index += 1;
        if (index != len(augmented[i])):
            divisor = augmented[i][index]
        if (index < len(augmented[i])):
            augmented = multiplyRow(augmented,i,1/(divisor*1.0))
    #clear pivot columns
    for j in xrange(len(matrix)):
        index = 0
        while(index < len(augmented) and not(almostEquals(augmented[j][index],1.0))):
            index+=1
        if (index != len(augmented[i])):
            for k in xrange(j):
                if (augmented[k][index] != 0):
                    multiple = -1.0 * augmented[k][index]
                    augmented = addMultipleOfRow(augmented,j,k,multiple)
    return augmented 

def matrixMultiply(a,b):
    try:
        assert len(b) == len(a[0])
    except:
        print "cannot multiply %d x %d and a %d x % d matrices together" %(len(a),len(a[0]),len(b),len(b[0]))
        assert(False)
    result = make2dList(len(a),len(b[0]))
    for i in xrange(len(result)):
        for j in xrange(len(result[0])):
            result[i][j] = dotProduct(a[i],extractColumn(b,j))
    return result

#solve a system of linear equations
def separateColumns(M):
    columns = set()
    for i in xrange(len(M)):
        for j in xrange(len(M[i])):
            if(almostEquals(M[i][j],1.0)):
                columns.add(j)
                break;
                #edit for row of zeroes
        
    result = []
    for k in xrange(len(M[0])):
        if (k not in columns):
            result += [k]
    return (result,list(columns))

def LU_Factorization(a):
    #gets the matrix in upper triangular form
    result = a
    i_matrix = makeIdentity(len(a),len(a))
    i = 0
    while (i<len(a)-1):
        #i is less than the number of rows in the column
        j = i+1
        #j starts from after the pivot
        while (j < len(a)):
            #go through all the columns after the pivot
            if (a[i][i] != 0):
                i_matrix[j][i] = float(a[j][i])/float(a[i][i])
            result = eliminateVariable(a,i,j,i)
            j+=1 
        i+=1
    return (i_matrix,result)
        
def solveMatrixSystem(A,b):
    #check dimensions
    try:
        assert(len(A) == len(b))
    except:
        print "No possible solution with given matrix dimensions"
        assert(False)
    #reduce the augmented matrix to echelon form    
    augmented = augmentedMatrix(A,b)
    augmented = reducedEchelonForm(augmented)
    solution = extractColumn(augmented,len(augmented[0])-1)
    matrix = separateMatrixFromAugmented(augmented,0,len(augmented[0])-1)
    colClass = separateColumns(matrix)
    freeCols = colClass[0]
    pivCols = colClass[1]
    for col in freeCols:
        for i in xrange(len(matrix)):
            matrix[i][col] *= -1
    
    specialSolution = make2dList(len(matrix[0]),len(freeCols))
    
    freeCount = 0
    for j in xrange(len(freeCols)):
    #for each free variable    
        count = 0
        for i in xrange(len(matrix[0])):
        #for every col in the matrix    
            if i in pivCols:
                specialSolution[i][j] = matrix[count][freeCols[j]]
                count+=1
            elif i == freeCols[freeCount]:
                specialSolution[i][j] = 1.0
                freeCount += 1
                break
                
    fullSol = [0.0 for i in xrange(len(matrix[0]))]
    count = 0
    for i in xrange(len(fullSol)):
        if i in pivCols:
            fullSol[i] = solution[count]
            count += 1;
                
    result = make2dList(len(specialSolution),len(specialSolution[0]))
    for i in xrange(len(result)):
        for j in xrange(len(result[0])):
                result[i][j] == specialSolution[i][j]
    return (fullSol,specialSolution)

#Matrix Inverse
def isInvertable(M):
    matrix = copy.deepcopy(M)
    matrix = reducedEchelonForm(matrix)
    for row in matrix:
        if isZeroVector(row):
            return False
    return True
    
def matrixInverse(matrix):
    assert(isInvertable(matrix))
    M = copy.deepcopy(matrix)
    lower = LU_Factorization(M)[0]
    upper = LU_Factorization(M)[1]
    identity = makeIdentity(len(M),len(M[0]))
    for l_i in xrange(len(lower)):
        for l_j in xrange(len(lower[0])):
            if (l_i != l_j):
                identity = addMultipleOfRow(identity,l_j,l_i,-lower[l_i][l_j])
  
    #reverse up
    for i in xrange(len(upper)):
        index = 0
        while (index < len(upper) and almostEquals(upper[i][index],0.0) ):
            index += 1;
        divisor = upper[i][index]
        if (index < len(upper)):
            upper = multiplyRow(upper,i,1/(divisor*1.0))
            identity = multiplyRow(identity,i,1/(divisor*1.0))
    #clear pivot columns
    for j in xrange(len(upper)):
        index = 0
        while(index < len(upper) and not(almostEquals(upper[j][index],1.0))):
            index+=1
        for k in xrange(j):
            if (upper[k][index] != 0):
                multiple = -1.0 * upper[k][index]
                upper = addMultipleOfRow(upper,j,k,multiple)
                identity = addMultipleOfRow(identity,j,k,multiple)
    return identity  

# Orthogonalality

def projectionMatrix(A):
    return scalarMultiply((matrixMultiply(A,transpose(A))),
                           1/float(matrixMultiply(transpose(A),A)[0][0]))

def projection(a,b):
    return matrixMultiply(projectionMatrix(a),b)   

#Graham-Schmidt Method
def QR_Factorization(matrix):
    Q = make2dList(len(matrix),len(matrix[0]))
    R = make2dList(len(matrix[0]),len(matrix[0]))
    v1 = extractColumn(matrix,0)
    R[0][0] = norm(v1)
    q0 = vecTo2d(normalize(v1))
    vectors = []
    vectors.append(q0)
    for i in xrange(1,min(len(matrix),len(matrix[0]))):
        qTemp = vecTo2d(extractColumn(matrix,i))
        for j in xrange(len(vectors)):
            scalar = (matrixMultiply(transpose(vectors[j]),qTemp))
            assert(scalar != None)
            scalar = scalar[0][0]
            R[j][i] = scalar
            qTemp = matrixSub(qTemp,scalarMultiply(vectors[j],scalar))
        assert(i==j+1)
        R[j+1][i] = norm(extractColumn(qTemp,0))
        vectors.append(normalize2d(qTemp))
    for i in xrange(len(vectors)):
        for j in xrange(len(vectors[0])):
            Q[i][j] = vectors[i][j][0]
    return (Q,R)
    
# Determinants

def minusMatrix(matrix,i,j):
    result = make2dList(len(matrix)-1,len(matrix[0])-1)
    rowCount = 0
    for row in xrange(len(matrix)):
        if (row == i):
            continue
        colCount = 0
        for col in xrange(len(matrix[0])):
            if (col != j):
                result[rowCount][colCount] = matrix[row][col]
                colCount+=1
        rowCount += 1
    return result
                
def det(matrix):
    #Checks
    if (len(matrix) != len(matrix[0])):
        return 0.0
    if len(matrix) == 1:
        return matrix[0][0]
    if (len(matrix) > 2):
        assert (len(matrix) == len(matrix[0]))
    #Calculation
    if (len(matrix) == 2 ):
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
    else:
        coFactorRow = matrix[0]
        for i in xrange(len(coFactorRow)):
            factor = 1 + -2*(i%2 == 1)
        return factor * coFactorRow[i] * det(minusMatrix(matrix,0,i))

def detFromCofactorMatrix(matrix,cofactor):
    det = 0
    coFactorRow = matrix[0]
    for i in xrange(len(coFactorRow)):
        det += cofactor[0][i] * coFactorRow[i]
    return det
    
def coFactorMatrix(matrix):
    if (len(matrix) > 2):
        assert len(matrix) == len(matrix[0])
    result = make2dList(len(matrix),len(matrix[0]))
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            result[i][j] = (1-2*((i+j)%2 == 1)) * det(minusMatrix(matrix,i,j))
    return result
    
def coFactorInverse(matrix):
    assert(isInvertable(matrix))
    C = coFactorMatrix(matrix)
    detA = detFromCofactorMatrix(matrix,C)
    assert (detA != 0)
    return scalarMultiply(transpose(C),1/float(detA))
    
#Eigenvalues and Eigenvectors

def nullSpace(M):
    solution = [0.0 for i in xrange(len(M))]
    return solveMatrixSystem(M,solution)

def rowSpace(M):
    matrix = reducedEchelonForm(M)
    rowSpace = []
    for row in matrix:
        for elem in row:
            if not(almostEquals(0.0,elem)):
                rowSpace.append(row)
                break
    return rowSpace

def columnSpace(M):
    return rowSpace(transpose(M))
        
def leftNullSpace(M):
    return nullSpace(traspose(M))     
        
def nthDegreeRegression(pointList, drg):
    #pointList is a list of points in form (x,y)
    degree = drg+1
    A = make2dList(len(pointList),degree)
    B = []
    for i in xrange(len(pointList)):
        B.append([pointList[i][1]])
        for j in xrange(degree):
            A[i][j] = ((pointList[i][0])**j)
    
    B = matrixMultiply(transpose(A),B)
    A = matrixMultiply(transpose(A),A)
    x = solveMatrixSystem(A,extractColumn(B,0))
    return x[0]

def polynomDerive(polynomial):
    #polynomial given as a set of coefficients
    derivative = make2dList(len(polynomial)-1,len(polynomial))
    for row in xrange(len(derivative)):
        for col in xrange(len(derivative[0])):
            if col == row+1:
                derivative[row][col] = col
                
    poly = make2dList(len(polynomial),1)
    for i in xrange(len(polynomial)):
        poly[i][0] = polynomial[i]
    
    result = matrixMultiply(derivative,poly)
    return (extractColumn(result,0))
    
def polynomIntegrate(polynomial):
    #polynomial given as a set of coefficients in increasing order
    integral = make2dList(len(polynomial)+1,len(polynomial))
    for row in xrange(len(integral)):
        for col in xrange(len(integral[0])):
            if (row == col+1 and row == 1):
                pass
            elif row == col+1:
                integral[row][col] = 1/float(col)
                
    poly = make2dList(len(polynomial),1)
    for i in xrange(len(polynomial)):
        poly[i][0] = polynomial[i]
           
    result = matrixMultiply(integral,poly)
    return (extractColumn(result,0))
