def selection_sort(numbers, list_size):
    i = 0
    while(i<list_size):
        smallest_number_index = i
        j = i+1
        while(j<list_size):
            if numbers[j] < numbers[smallest_number_index]:
                smallest_number_index = j
                numbers[i], numbers[smallest_number_index] = numbers[smallest_number_index],numbers[i],
            j += 1
        i += 1
        
    return numbers

def cal_selection_sort():
    list_size = int(input("Enter Length of list: "))
    if list_size < 1:
        print('Enter list size greater than 0, Try again!')
        cal_selection_sort()
        return

    numbers = []
    i = 0
    while(i<list_size):
        numbers += [int(input('Enter number: '))]
        i += 1

    print(*selection_sort(numbers, list_size))
cal_selection_sort()
