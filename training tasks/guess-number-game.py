import random 
def is_same(computer_generated_number, user_input):
    if computer_generated_number == user_input:
        return 1
    
    cows = 0
    bulls = 0

    computer_generated_number = list(map(int, list(str(computer_generated_number)))) 
    user_input = list(map(int, list(user_input)))

    # counting perfect place (cows)
    for i in range(4):
        if user_input[i] == computer_generated_number[i]:
            cows += 1
            computer_generated_number[i] = '-'
            user_input[i] = '-'
            
    # counting wrong places (bulls) 
    for i in range(4):
        if user_input[i] in computer_generated_number and user_input[i] != '-':
            bulls += 1
            computer_generated_number[computer_generated_number.index(user_input[i])] = '-'
    print(f"{cows} cows, {bulls} bulls")
    return 0
    
def start_game():
    computer_generated_number = str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))
    # computer_generated_number = '2213'
    counter = 0
    while True:
        user_input = input('Enter Four digit number: ')
        if len(user_input) != 4 or not user_input.isnumeric():
            print('Invalid input, You must enter 4 digits. Try again!')
            continue

        counter += 1

        if is_same(computer_generated_number, user_input):
            break

    print(f"\nwhorayy, guesses: {counter}")

start_game()
