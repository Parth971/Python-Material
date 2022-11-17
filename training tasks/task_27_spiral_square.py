def display(lis):
    for i in lis:
        for j in i:
            print("{:<3}".format(j), end=" ")
        print()


if __name__ == '__main__':
	while True:
		print("Enter height: ")
		user_input1 = input()

		print("Enter width: ")
		user_input2 = input()
		height, width = user_input1, user_input2

		if height.isdigit() and width.isdigit() and int(height) > 0 and int(width) > 0:

			height, width = int(height), int(width)
			lis = [[0]*width for i in range(height)]

			counter = 1
			direction = 1 # 1-> left to right, 2-> top to bottom, 3-> right to left, 4-> bottom to top
			top = 0
			bottom = height-1
			left = 0
			right = width-1

			while(counter <= (height*width)):
			    if direction == 1:
			        for i in range(left, right+1):
			            lis[top][i] = counter
			            counter += 1
			        top += 1
			    elif direction == 2:
			        for i in range(top, bottom+1):
			            lis[i][right] = counter
			            counter += 1
			        right-=1
			    elif direction == 3:
			        for i in range(right, left-1, -1):
			            lis[bottom][i] = counter
			            counter += 1
			        bottom-=1
			    else:
			        for i in range(bottom, top-1, -1):
			            lis[i][left] = counter
			            counter += 1
			        left+=1
			    direction = (direction + 1) % 4
			    
			print(f"Spiral Square:")
			display(lis)
		else:
			print('Invalid!!')


		if input('Enter y to exit.') == 'y':
			break
