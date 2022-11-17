def add_value(row, col):
    matrix = []
    i = 0
    while(i<row):
        temp = []
        j = 0
        while(j<col):
            temp += [int(input('Enter number: '))]
            j += 1
        i += 1
        matrix += [temp]
    return matrix

def display_matrix(matrix, row, col):
    i = 0
    while(i<row):
        j = 0
        while(j<col):
            print(matrix[i][j], end=' ')
            j += 1
        print()
        i += 1
        
def matrix_multiplication(matrix1, matrix2, r1, c1, r2, c2):
    matrix = []
    i = 0
    while(i<r1):
        temp = []
        j = 0
        while(j<c2):
            temp += [0]
            j += 1
        i += 1
        matrix += [temp]
    i = 0
    while(i<r1):
        j = 0
        while(j<c2):
            k = 0
            while(k<c1):
                matrix[i][j] += matrix1[i][k] * matrix2[k][j]
                k += 1
            j += 1
        i += 1
    return matrix
    
def cal_matrix_multiplication():
    r1 = int(input('Enter number of rows for Matrix 1: '))
    
    if r1 < 1:
        print('Row number must be greater than 0, Try again!')
        cal_matrix_multiplication()
        return
    
    c1 = int(input('Enter number of columns for Matrix 1: '))
    
    if c1 < 1:
        print('Column number must be greater than 0, Try again!')
        cal_matrix_multiplication()
        return
    
    print("Enter values of Matrix 1: ")
    matrix1 = add_value(r1,c1)
    print('Matrix 1: ')
    display_matrix(matrix1, r1, c1)


    r2 = int(input('Enter number of rows for Matrix 2: '))
    
    if r2 < 1:
        print('Row number must be greater than 0, Try again!')
        cal_matrix_multiplication()
        return
    if c1 != r2:
        print('Column number of first matrix and Row number of second matrix must be same, Try again!')
        cal_matrix_multiplication()
        return

    c2 = int(input('Enter number of columns for Matrix 2: '))
    
    if c2 < 1:
        print('Column number must be greater than 0, Try again!')
        cal_matrix_multiplication()
        return
    
    
    print("Enter values of Matrix 2: ")
    matrix2 = add_value(r2,c2)
    print('Matrix 2: ')
    display_matrix(matrix2, r2, c2)
    
    result = matrix_multiplication(matrix1, matrix2, r1, c1, r2, c2)
    print('Result Matrix: ')
    display_matrix(result, r1, c2)
    
cal_matrix_multiplication()
