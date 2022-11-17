def makediamond(total_height):
    if total_height < 1:
        print("Minimum height should be 1 and should be odd value, if even value given then it will return one more heighted tree")
        return 
    
    if total_height%2==0:
        total_height += 1
    
    top_traingle_height = (total_height-1) // 2
    bottom_traingle_height = (total_height-1) // 2
    
    # top traingle
    for i in range(top_traingle_height):
        for j in range(top_traingle_height-i):
            print(' ', end=" ")
        middle = (i+1)*2-1
        for j in range(middle):
            print('*', end=" ")
        print('')
    
    print('* '* total_height)
        
    # bottom traingle
    for i in range(bottom_traingle_height):
        for j in range(i+1):
            print(' ', end=" ")
        middle = (bottom_traingle_height-i-1)*2+1
        for j in range(middle):
            print('*', end=" ")
        print('')



if __name__ == '__main__':
    while True:
        height = input('Enter tree height')

        if height.isdigit() and int(height) > 0:
            height = int(height)
            makediamond(height)

        else:
            print('Invalid!')

        if input('Enter y to exit.') == 'y':
            break
