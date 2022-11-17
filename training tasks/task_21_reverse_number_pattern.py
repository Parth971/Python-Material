if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:
			height = int(height)
			for i in range(height):
			    for j in range(1, height-i+1):
			        print(j, end=" ")
			    print('')

		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
