def insertion_sort(numbers, list_size):
    i = 1
    while(i<list_size):
        temp = i - 1
        while temp >= 0:
            if numbers[temp] > numbers[temp + 1]:
                numbers[temp], numbers[temp + 1] = numbers[temp + 1], numbers[temp]
            temp -= 1
        i += 1
    return numbers

def cal_insertion_sort():
    list_size = int(input("Enter Length of list: "))
    if list_size < 1:
        print('Enter list size greater than 0, Try again!')
        cal_insertion_sort()
        return

    numbers = []
    i = 0
    while(i<list_size):
        numbers += [int(input())]
        i += 1
    
    print(insertion_sort(numbers, list_size))
cal_insertion_sort()
