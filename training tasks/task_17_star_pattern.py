if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:

			for i in range(int(height)):
				print('*'*(i+1))
		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
