if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:
			height = int(height)
			for i in range(height):
			    for j in range(height-i-1):
			        print(' ', end=" ")
			    middle = (i+1)*2-1
			    for j in range(i+1, middle):
			        print(j, end=" ")
			    print(middle, end=" ")
			    for j in range(middle-1, i, -1):
			        print(j, end=" ")
			    print('')



		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
