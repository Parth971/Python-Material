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

# global
total = 0
def determinant_recursive(A, row, col):
    global total
    
    if row == 2 and col == 2:
        result = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return result
 
    current_column = 0
    while(current_column<row):
        Asub = A[1:]
        height = row-1
        i = 0
        while(i<height):
            Asub[i] = Asub[i][0:current_column] + Asub[i][current_column+1:]
            i += 1
            
        sign = (-1) ** (current_column % 2)
        sub_det = determinant_recursive(Asub, row-1, col-1)
        total += sign * A[0][current_column] * sub_det 
        current_column += 1
 
    return total
def cal_determinant():
    size = int(input('Enter row number(or column number): '))
    matrix = add_value(size, size)
    print('Matrix is : ')
    display_matrix(matrix, size, size)
    result = determinant_recursive(matrix, size, size)
    print(f'determinat is {result}')
    
cal_determinant()
