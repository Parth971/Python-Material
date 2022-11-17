def factors(number):
    lis = []
    
    i = 1
    while(i*i <= number):
        if number % i == 0:
            lis.append(i)
            if number//i != i:
                lis.append(number//i)
        i += 1

    return sorted(lis)

if __name__ == '__main__':
    while True:
        user_input = input('Enter number for which you want to find factors')
        if user_input.isdigit() and int(user_input) > 0:
            print(*factors(int(user_input)))
        else:
            print('Invalid!!')

        user_input = input('\nEnter y to exit.')
        if user_input == 'y':
            print('Exit')
            break
