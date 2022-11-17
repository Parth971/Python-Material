if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:
			height = int(height)
			counter = 1
			for i in range(height):
			    for j in range(i+1):
			        print(counter, end=" ")
			        counter+=1
			    print()
		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
