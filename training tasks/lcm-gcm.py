def isprime(number):
    if number == 1:
        return False

    i = 2
    while i*i <= number:
        if number % i == 0:
            return False
        i += 1
    return True

def lcm(num1, num2):
    greatest = max(num1, num2)
    lowest = min(num1, num2)
    i = greatest

    print(isprime(lowest))
    if i%lowest != 0 and isprime(lowest):
        return lowest*greatest

    print('while')
    while True:
        if i%lowest == 0:
            return i
        i += greatest


def gcd(num1, num2):
    if num2 != 0:
        return gcd(num2, num1 % num2)
    else:
        return num1

if __name__ == '__main__':
    while(True):
        print("\n\nEnter Two numbers")
        num1 = input('Enter first number: ')
        num2 = input('Enter second number: ')
        if num1.isdigit() and num2.isdigit():
            num1, num2 = int(num1), int(num2)
            if num1<1 or num2<1:
                print("Number not Valid.")
                continue
            print(f"LCM is {lcm(num1, num2)}")
            print(f"GCD is : {gcd(num1, num2)}")
        else:
            print('Enter numeric value.!!')

        user_input = input('\nEnter y to exit.')
        if user_input == 'y':
            print('Exit')
            break
