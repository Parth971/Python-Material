if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:
			height = int(height)
			for i in range(height):
			    for j in range(i):
			        print(' ', end=" ")
			    middle = (height-i)*2-1
			    for j in range(middle):
			        print('*', end=" ")
			    print('')


		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
