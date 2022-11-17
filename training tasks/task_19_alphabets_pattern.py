if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:

			letter = ord('A')
			for i in range(int(height)):
			    for j in range(1, i+2):
			        print(chr(letter+i), end=" ")
			    print('')

		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
