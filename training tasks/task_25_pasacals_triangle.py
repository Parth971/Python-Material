#       0 1 ->starting value   
#      0 1 0
#     0 1 1 0
#    0 1 2 1 0
#   0 1 3 3 1 0
#  0 1 4 6 4 1 0
# 0 1 5 10 10 5 1 0



def get_next_elements(ele_list):
    new_ele_list = [0]
    for i in range(len(ele_list)-1):
        new_ele_list.append( int(ele_list[i]) + int(ele_list[i+1]) )
    
    new_ele_list.append(0)
    return new_ele_list

if __name__ == '__main__':
	while True:
		height = input('Enter tree height')

		if height.isdigit() and int(height) > 0:
			height = int(height)
			ele_list = [0, 1]
			all_element = []
			for i in range(height):
			    ele_list = get_next_elements(ele_list)
			    all_element.append(ele_list[1:-1])

			for i in range(height):
			    for j in range(height-i-1):
			        print(' ', end='')
			    for j in all_element[i]:
			        print(j, end=' ')
			    print()




		else:
			print('Invalid!')

		if input('Enter y to exit.') == 'y':
			break
