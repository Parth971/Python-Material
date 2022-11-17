def isPalindrome(number):
    temp=number
    reverse_number=0
    while(number>0):
        digit=number%10
        reverse_number=(reverse_number*10)+digit
        number=number//10
    if(temp==reverse_number):
        print("Yes, it is palindrome")
    else:
        print("No, it's not palindrome")

isPalindrome(int(input("Enter number to check if it is palindrome or not: ")))
