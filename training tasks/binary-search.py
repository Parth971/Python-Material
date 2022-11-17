def selection_sort(numbers, list_size):
    i = 0
    while(i<list_size):
        smallest_number_index = i
        j = i+1
        while(j<list_size):
            if numbers[j] < numbers[smallest_number_index]:
                smallest_number_index = j
            j += 1
        numbers[i], numbers[smallest_number_index] = numbers[smallest_number_index], numbers[i]
        i += 1
    return numbers

def binary_search(numbers, num, low, high):
    if high>=low:
        mid = (high+low)//2
        if(numbers[mid] == num):
            return mid
        if(num < numbers[mid]):
            return binary_search(numbers, num, 0, mid-1)
        if(num > numbers[mid]):
            return binary_search(numbers, num, mid+1, high)
    return -1
    

def cal_binary_search():
    list_size = int(input("Enter Length of list: "))

    if list_size < 1:
        print('Enter list size greater than 0, Try again!')
        cal_binary_search()
        return

    print("Enter numbers: ")
    
    numbers = []
    
    i = 0
    while(i<list_size):
        numbers += [int(input())]
        i += 1

    num = int(input("Enter number to be searched: "))

    numbers = selection_sort(numbers, list_size)
    result = binary_search(numbers, num, 0, list_size-1)
    print(f"{num} is present at {result+1} position in {numbers}") if result != -1 else print(f"{num} is not present in {numbers}")

cal_binary_search()
