def rearrange(arr):
    n = len(arr)
    for i in range(n):
        arr[arr[i]%n] = arr[arr[i]%n] + i * n
    
    for i in range(n):
        arr[i] = arr[i] // n

if __name__ == '__main__':
    while True:
        length = input('Enter length of array: ')
        if length.isdigit() and int(length) > 1:
            length = int(length)
        else:
            print('Enter valid number!!!')
            continue
        
        arr = []
        i = 0
        while(i < length):
            num = input(f'Enter Element({i+1}): ')
            if num.isdigit() and int(num) >= 0 and int(num) < length and int(num) not in arr:
                arr.append(int(num))    
                i += 1  
            else:
                print('Invalid!')
                continue
        
        print(f"Input array is {arr}")
        rearrange(arr)
        print(f"Final array is {arr}")

        user_input = input('\nEnter y to exit.')
        if user_input == 'y':
            print('Exit')
            break
