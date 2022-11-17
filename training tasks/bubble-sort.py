def bubble_sort(numbers, list_size):
    i = 0
    while(i<list_size-1):
        swaped = 0
        j = 0
        while(j<list_size-i-1):
            if numbers[j] > numbers[j + 1]:
                swaped = 1
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
            j += 1
        if not swaped:
            break
        i += 1
        
    return numbers

def cal_bubble_sort():
    list_size = int(input("Enter Length of list: "))
    if list_size < 1:
        print('Enter list size greater than 0, Try again!')
        cal_bubble_sort()
        return

    numbers = []
    i = 0
    while(i<list_size):
        numbers += [int(input('Enter number: '))]
        i += 1

    print(*bubble_sort(numbers, list_size))
cal_bubble_sort()
