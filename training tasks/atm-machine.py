import random

def authenticate_admin():
    ''' This funtion asks for password of admin
    and returns authentication flag. '''
        
    password = input('Enter admin password: ')
    
    if MAIN_ADMIN_PASSWORD == password:
        print('Password matched..')
        return 1
    
    print('Password is incorrect!! Try again.')
    return 0

def authenticate(users):
    ''' This funtion asks for card number and pin number of user 
    and returns tuple of card_number and authentication flag. '''
    
        
    input_card_number = input('Enter Card number: ')
    input_pin = input('Enter Pin: ')
    user = users.get(input_card_number, None)
    
    if user:
        if user['pin_number'] == input_pin:
            return(input_card_number, 1)
        print("Pin number didn't matched.")
        return(None, 0)
    else:
        print("User not found OR Card number is incorrect.")
        return(None, 0)

def create_bank(banks, bank_admins):
    ''' This function asks for bank name and adds in banks list. '''

    if not authenticate_admin():
        print('Admin authentication failed!!')
        return banks, bank_admins

    user_input = input('Enter Bank Name:')

    user_input = user_input.upper()

    if user_input not in banks:
        bank_admins[user_input] = '-'
        banks.append(user_input)
        print(f'Bank: {user_input} is created successfully.')
    else:
        print("Bank Already Exists. Try again!")
    return banks, bank_admins

def create_atm(banks, atms, INITIAL_ATM_BALANCE, bank_admins):
    ''' This function asks for bank name of atm and Location (ie. city) of ATM
    and adds to atms list. '''
    
        
    if not banks:
        print("No Banks Created Yet. First Create Bank then try again for creating its ATM.")
        return atms
    
    print("Select Bank for creating its ATM: ")
    for i, bank in enumerate(banks):
        print(f"{i+1}. {bank}")
    
    user_input = input()
    if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return atms
    
    bank_name = banks[int(user_input)-1]
    
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return atms
        
    print(f"Enter Location where you want ATM of {bank_name}.")
    user_input = input()
    atm_location = user_input
    atms.append([bank_name, atm_location, INITIAL_ATM_BALANCE])
    print(f"ATM created successfully.\nBank Name : {bank_name}\nATM location : {atm_location}\nInitial Balance: {INITIAL_ATM_BALANCE}")
    
    return atms

def create_user_account(banks, users, INITIAL_USER_BALANCE, bank_admins):
    ''' This function asks for bank name and generates card_number and pin number. 
    Then adds to user dictionary. '''

    
    if not banks:
        print("No Banks Available.")
        return users
    
    print("Select Bank for creating account: ")
    for i, bank in enumerate(banks):
        print(f"{i+1}. {bank}")
    
    user_input = input()
    if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return users
    
    bank_name = banks[int(user_input)-1]
    
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return users
    
    user_name = input('Enter user name: ')
    card_number = bank_name + "@" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    pin_number = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
    
    users[card_number] = {'user_name':user_name,'bank_name' : bank_name,
                         'pin_number' : pin_number, 'amount' : INITIAL_USER_BALANCE}
    print(f"User Account has been successfully created.\nUser Name: {user_name}\nBank Name: {bank_name}\nUser Card Number: {card_number}\nUser Pin number: {pin_number}")
    print("Use this credentials for transactions and viewing acoount details. Do not Share this with any one.")
    
    return users

    
def withdraw_money(atms, users, transcation_history, MAX_TRANSACTION, MAX_TRANSACTION_AMOUNT):
    ''' This function lets user to select atm from available atms.
    Authenticates user and checks for transcation limit then withdraw money.  '''

    
    if not atms:
        print("No ATMs available.")
        return atms, users, transcation_history
    
    print("Select one of the atms: ")
    for i, atm in enumerate(atms):
        print(f"{i+1}. {atm[0]} located at {atm[1]}")
        
    user_input = input()
    if (not user_input.isnumeric()) or int(user_input) > len(atms) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return atms, users, transcation_history
    
    current_atm_index = int(user_input)-1
    current_user_input_card_number, authenticated = authenticate(users)
        
    if authenticated:
        if transcation_history.get(current_user_input_card_number,0) == 0:
            transcation_history[current_user_input_card_number] = {'total_transaction_number': 0, 'total_transaction_amount': 0}
        
        if transcation_history[current_user_input_card_number]['total_transaction_number'] >= MAX_TRANSACTION:
            print("You have reached daily transaction limit.")
            return atms, users, transcation_history

        input_amount = input('Enter Amount to be withdrawed:')
        if not input_amount.isnumeric():
            print("Amount should be numeric. Enter Again.")
            return atms, users, transcation_history
            
        input_amount = int(input_amount)
        
        if input_amount > 25000 or input_amount < 100:
            print("You Cannot withdraw less than Rs. 100 and more than Rs. 25,000 in single transaction.")
            return atms, users, transcation_history
        
        if atms[current_atm_index][2] < input_amount:
            print(f'Atm dont have enough money.')
            return atms, users, transcation_history
        
        available_transaction_amount_for_day = MAX_TRANSACTION_AMOUNT-transcation_history[current_user_input_card_number]['total_transaction_amount']
        if input_amount > available_transaction_amount_for_day:
            print('Limit exceeded!')
            print(f"You cannot get Rs.{input_amount} amount. Total available transaction amount is {available_transaction_amount_for_day}")
            return atms, users, transcation_history
        
        if users[current_user_input_card_number]['bank_name'] != atms[current_atm_index][0]:
            input_amount = input_amount + (input_amount*0.05)
        
        if users[current_user_input_card_number]['amount'] >= input_amount:
            
            users[current_user_input_card_number]['amount'] -= input_amount
            
            transcation_history[current_user_input_card_number]['total_transaction_amount'] += input_amount-(input_amount*0.05)
            transcation_history[current_user_input_card_number]['total_transaction_number'] += 1
            
            if users[current_user_input_card_number]['bank_name'] != atms[current_atm_index][0]:
                print(f"Successfully deducted. In hand Rs.{input_amount/1.05}.\nMoney deducted from account {input_amount}.\nTotal balance is {users[current_user_input_card_number]['amount']}.")
            else:
                print(f"Successfully deducted Rs.{input_amount}. Total balance is {users[current_user_input_card_number]['amount']}.")
            
            atms[current_atm_index][2] -= input_amount
        else:
            print("Not Enough Money in Your Account OR May be this atm is charging you 5% more that input amount which is not present in your account!!")
    else:
        print("Authentication Failed. Try again!")
    
    return atms, users, transcation_history
        
def deposit_money(atms, users, transcation_history, MAX_TRANSACTION):
    ''' This function lets user to select atm from available atms.
    Authenticates user and checks for transcation limit then deposits money.  '''

    
    if not atms:
        print("No ATMs available.")
        return atms, users, transcation_history
    
    print("Select one of the atms: ")
    for i, atm in enumerate(atms):
        print(f"{i+1}. {atm[0]} located at {atm[1]}")
        
    user_input = input()
    if (not user_input.isnumeric()) or int(user_input) > len(atms) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return atms, users, transcation_history
    
    current_atm_index = int(user_input)-1

    current_user_input_card_number, authenticated = authenticate(users)
    
    if authenticated:
        if transcation_history.get(current_user_input_card_number,0) == 0:
            transcation_history[current_user_input_card_number] = {'total_transaction_number': 0, 'total_transaction_amount': 0}
        
        if transcation_history[current_user_input_card_number]['total_transaction_number'] >= MAX_TRANSACTION:
            print("You have reached daily transaction limit.")
            return atms, users, transcation_history
            
        print("Enter Amount to be Deposited: ")
        
        input_amount = input()
        if not input_amount.isnumeric():
            print("Amount should be numeric. Enter Again.")
            return atms, users, transcation_history
            
        input_amount = int(input_amount)
        if input_amount < 100 and input_amount > 25000:
            print("You Cannot deposite less than Rs. 100 and more than Rs. 25,000 in single transaction.")
            return atms, users, transcation_history
        
        atms[current_atm_index][2] += input_amount
        users[current_user_input_card_number]['amount'] += input_amount
        transcation_history[current_user_input_card_number]['total_transaction_number'] += 1
        print(f"Successfully Deposited Rs.{input_amount}. Total balance is {users[current_user_input_card_number]['amount']}.")
    else:
        print("Authentication Failed. Try again!")
    
    return atms, users, transcation_history
        
def view_user_details(users):
    ''' This function authenticates user and gives user details. '''
    
        
    current_user_input_card_number, authenticated = authenticate(users)
    if authenticated:
        print(f"Bank Name : {users[current_user_input_card_number]['bank_name']}")
        print(f"Card Number : {current_user_input_card_number}")
        print(f"Pin Number : {users[current_user_input_card_number]['pin_number']}")
        print(f"Amount : {users[current_user_input_card_number]['amount']}")
    else:
        print("Authentication Failed")

def update_user_details(banks, users, bank_admins, remove_account=False):
    ''' This function authenticates user and lets user updated or delete account.  '''

    
    if not users:
        print("No Users Available.")
        return users
    
    current_user_input_card_number, authenticated = authenticate(users)
    if authenticated:
        bank_name = users[current_user_input_card_number]['bank_name']
    
        if (remove_account):
            if not authenticate_admin():
                print('Admin authentication failed!!')
                return users

            if users[current_user_input_card_number]['amount'] != 0:
                print('This user account has some money, so cannot be deleted. First clear account by withdrawing all money.')
                return users

            del users[current_user_input_card_number]
            print("User Successfully deleted.")
            
            return users
        
        user_input = input('\nWhat do you want to update?\n1. Bank Name\n2. Card number\n3. Pin Number\n4. User Name')
        if user_input == '1':
            curret_bank_name = users[current_user_input_card_number]['bank_name']
            print('Enter password for current bank admin: ')
            if not authenticate_admin():
                print('Admin authentication failed!!')
                return users

            print("Select one of the banks: ")
            for i, bank in enumerate(banks):
                print(f"{i+1}. {bank}")
                
            user_input = input()
            if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
                print("Number not Valid. Try again!")
                return users

            bank_name = banks[int(user_input)-1]

            users[current_user_input_card_number]['bank_name'] = bank_name
            
            new_card_number = bank_name + '@' + ''.join(current_user_input_card_number.split('@')[1:])
            old_card_data = users[current_user_input_card_number]
            del users[current_user_input_card_number]
            users[new_card_number] = old_card_data
            print(f"Card number successfully Updated. New Card number is {new_card_number}")
            print(f"Bank name successfully Updated. New bank Name is {bank_name}")
        elif user_input == '2':
            new_card_number = users[current_user_input_card_number]['bank_name'] + "@" + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
            old_card_data = users[current_user_input_card_number]
            del users[current_user_input_card_number]
            users[new_card_number] = old_card_data
            print(f"Card number successfully Updated. New Card number is {new_card_number}")
        elif user_input == '3':
            new_pin_number = str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9)) + str(random.randint(0,9))
            users[current_user_input_card_number]['pin_number'] = new_pin_number
            print(f"Pin Number successfully Updated. New Pin number is {new_pin_number}")
        elif user_input == '4':
            new_user_name = input('Enter new user name: ')
            users[current_user_input_card_number]['user_name'] = new_user_name
            print(f'User name successfully changed to {new_user_name}')
        else:
            print('Number not Valid. Try again')

    else:
        print("Authentication Failed. Try again!")

    return users

def update_atm_details(banks, atms, bank_admins, remove_atm=False):
    ''' This function lets user update atm location and bank name. '''

    
    if not atms:
        print("No ATMs available.")
        return atms
    
    print("Select one of the atms: ")
    for i, atm in enumerate(atms):
        print(f"{i+1}. {atm[0]} located at {atm[1]}")
        
    user_input = input()
    
    if (not user_input.isnumeric()) or int(user_input) > len(atms) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return atms
    
    bank_name = atms[int(user_input)-1][0]
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return atms
    
    if remove_atm:
        atms.pop(int(user_input)-1)
        print("ATM Successfully deleted.")
        return atms
    
    current_atm_index = int(user_input)-1
    print("\nWhat do you want to update?\n1. Bank Name\n2. Location")
    user_input = input()
    
    if user_input == '1':
        print("Select one of the banks: ")
        for i, bank in enumerate(banks):
            print(f"{i+1}. {bank}")
        
        user_input = input()
        
        if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
            print("Number not Valid. Try again!")
            return atms
        
        bank_name = banks[int(user_input)-1]

        atms[current_atm_index][0] = bank_name
        print(f"Bank name successfully Updated. New bank Name is {bank_name}")
    elif user_input == '2':
        new_location = input('What you want to be new location of this ATM?')
        atms[current_atm_index][1] = new_location
        print(f"Location successfully Updated. New Location is {new_location}")
    else:
        print('Number not Valid. Try again!')

    return atms

def insert_money(atms, bank_admins):
    ''' This function lets select atm and add money to it. '''

    
    if not atms:
        print("No ATMs available.")
        return atms
    
    print("Select one of the atms: ")
    for i, atm in enumerate(atms):
        print(f"{i+1}. {atm[0]} located at {atm[1]}")
        
    user_input = input()
    if not user_input.isnumeric() or int(user_input) > len(atms) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return atms
    
    current_atm_index = int(user_input)-1
    
    bank_name = atms[current_atm_index][0]
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return atms
    
    user_input = input('Enter amount to be inserted:')
    if not user_input.isnumeric() or int(user_input)<=0:
        print("Amount not Valid. Try again!")
        return atms
    
    atms[current_atm_index][2] += int(user_input)
    print(f"Successfully inserted Rs. {user_input} in ATM of {atms[current_atm_index][0]} bank located at {atms[current_atm_index][1]}.\nTotal amount is {atms[current_atm_index][2]}")                  
            
    return atms

def delete_bank(banks, atms, users, bank_admins):
    ''' This function lets user delete bank. '''

    
    if not banks:
        print("No Banks Available.")
        return banks, atms, users, bank_admins
    
    print("Select Bank: ")
    for i, bank in enumerate(banks):
        print(f"{i+1}. {bank}")
        
    user_input = input()
    
    if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return banks, atms, users, bank_admins
    
    bank_name = banks[int(user_input)-1]
    
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return banks, atms, users, bank_admins
    
    temp = list(users.keys())
    for users_card_number in temp:
        if users[users_card_number]['bank_name'] == bank_name:
            print(f'Some users are present of this bank, so bank: {bank_name} cannot be deleted. First remove users.')
            return banks, atms, users, bank_admins
        
    for atm in atms:
        if atm[0] == bank_name:
            print(f'Some ATMs are present of this bank, so bank: {bank_name} cannot be deleted. First delete ATM"s.')
            return banks, atms, users, bank_admins
    
    banks.pop(int(user_input)-1)
    del bank_admins[bank_name]
    print(f"{bank_name} is deleted successfully.")

    return banks, atms, users, bank_admins

def update_bank(banks, atms, users, bank_admins):
    ''' This function lets user update bank. '''

    
    if not banks:
        print("No Banks Available.")
        return banks, atms, users, bank_admins
    
    print("Select Bank: ")
    for i, bank in enumerate(banks):
        print(f"{i+1}. {bank}")
        
    user_input = input()
    
    if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return banks, atms, users, bank_admins
    
    bank_name = banks[int(user_input)-1]
    
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return banks, atms, users, bank_admins
    
    user_input = input('Select options:\n1.Update Bank name')
    
    if user_input == '1':
        list_without_bank = [bank for bank in banks if bank != bank_name]
    
        user_input = input('Enter new name for bank: ')
        user_input = user_input.upper()
        if user_input in list_without_bank:
            print('This bank already exists, cant update bank name.')
            return banks, atms, users, bank_admins

        new_bank_name = user_input
        banks = list_without_bank + [new_bank_name]

        temp = list(users.keys())
        for users_card_number in temp:
            users[users_card_number]['bank_name'] = new_bank_name
            old_data = users[users_card_number]
            del users[users_card_number]
            new_card_number = new_bank_name + '@' + ''.join(users_card_number.split('@')[1:])
            users[new_card_number] = old_data

        for i in range(len(atms)):
            if atms[i][0] == bank_name:
                atms[i][0] = new_bank_name
        
        old_bank_data = bank_admins[bank_name]
        del bank_admins[bank_name]
        bank_admins[new_bank_name] = old_bank_data
        print('Bank name successfully Updated to', new_bank_name)
    else:
        print('Invalid Update. Try again!')
    
    return banks, atms, users, bank_admins

def view_atm(atms, bank_admins):
    ''' This function lets admin view atm. '''


    if not atms:
        print("No ATMs available.")
        return
    
    print("Select one of the atms: ")
    for i, atm in enumerate(atms):
        print(f"{i+1}. {atm[0]} located at {atm[1]}")
        
    user_input = input()
    if (not user_input.isnumeric()) or int(user_input) > len(atms) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return
    
    current_atm_index = int(user_input)-1

    bank_name = atms[current_atm_index][0]
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return

    print('Atm details: ')
    print(f'Atm Bank name: {bank_name}')
    print(f'Atm Location: {atms[current_atm_index][1]}')
    print(f'Atm Amount: {atms[current_atm_index][2]}')


def view_all_users(banks, atms, users, bank_admins):
    ''' This function lets view all banks bank. '''

    
    if not banks:
        print("No Banks Available.")
        return
    
    print("Select Bank: ")
    for i, bank in enumerate(banks):
        print(f"{i+1}. {bank}")
        
    user_input = input()
    
    if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return
    
    bank_name = banks[int(user_input)-1]
    
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return

    temp = list(users.keys())
    ctr = 1
    no_user = True
    for users_card_number in temp:
        if users[users_card_number]['bank_name'] == bank_name:
            no_user = False
            print(f"\n{ctr}.\nCard Number : {users_card_number}")
            print(f"Bank Name : {users[users_card_number]['bank_name']}")
            print(f"Pin Number : {users[users_card_number]['pin_number']}")
            print(f"Amount : {users[users_card_number]['amount']}")
            ctr += 1
    if no_user:
        print('No users!')

def view_all_atms(banks, atms, bank_admins):
    ''' This function lets admin view atm. '''


    if not banks:
        print("No Banks Available.")
        return
    
    print("Select Bank: ")
    for i, bank in enumerate(banks):
        print(f"{i+1}. {bank}")
        
    user_input = input()
    
    if (not user_input.isnumeric()) or int(user_input) > len(banks) or int(user_input) <= 0:
        print("Number not Valid. Try again!")
        return
    
    bank_name = banks[int(user_input)-1]
    
    if not authenticate_admin():
        print('Admin authentication failed!!')
        return

    if not atms:
        print("No ATMs available.")
        return
    
    ctr = 1
    for atm in atms:
        if atm[0] == bank_name:
            print(f'\n{ctr}.\nAtm Bank name: {bank_name}')
            print(f'Atm Location: {atm[1]}')
            print(f'Atm Amount: {atm[2]}')
            ctr += 1

def run_atm(banks, atms, users, bank_admins, transcation_history, MAX_TRANSACTION, MAX_TRANSACTION_AMOUNT, INITIAL_ATM_BALANCE, INITIAL_USER_BALANCE):
    instructions = f'''
    -> Here, first we create Bank 
    -> Then we can create users and ATMs related to that bank
    -> Then with user credentials, user can withdraw or deposite money into/from bank account via any atms
    -> For withdrawls, user must be carefull about amount because withdrawl of money from atm of other banks can 
    cause 5% chrges.
    -> For deposites, user can deposite using any atms to his account
    -> update is same as Delete Bank and recreate bank because here banks is just list of bank names(strings)
        '''
    print(f"Welcome to system. \n {instructions}")
    
    while True:
        print('\nMenu')
        print('1. Withdraw Money\n2. Deposit money\n3. Create\n4. Update\n5. Delete\n6. Insert Money in ATM\n7. View\n8. Quit')
        user_input = input()

        if user_input == '1':
            atms, users, transcation_history = withdraw_money(atms, users, transcation_history, MAX_TRANSACTION, MAX_TRANSACTION_AMOUNT)
        elif user_input == '2':
            atms, users, transcation_history = deposit_money(atms, users, transcation_history, MAX_TRANSACTION)
        elif user_input == '3':
            print('\nCreate Menu')
            print('1. Create Bank\n2. Create ATM\n3. Create User Account\n4. Go back')
            user_input = input()

            if user_input == '1':
                banks, bank_admins = create_bank(banks, bank_admins)
            elif user_input == '2':
                atms = create_atm(banks, atms, INITIAL_ATM_BALANCE, bank_admins)
            elif user_input == '3':
                users = create_user_account(banks, users, INITIAL_USER_BALANCE, bank_admins)
            elif user_input == '4':
                continue
            else:
                print('Option not valid. Try again!!!')
        elif user_input == '4':
            print('\nUpdate Menu')
            print('1. Update Bank\n2. Update ATM\n3. Update User Account\n4. Go back')
            user_input = input()

            if user_input == '1':
                banks, atms, users, bank_admins = update_bank(banks, atms, users, bank_admins)
            elif user_input == '2':
                atms = update_atm_details(banks, atms, bank_admins)
            elif user_input == '3':
                users = update_user_details(banks, users, bank_admins)
            elif user_input == '4':
                continue
            else:
                print('Option not valid. Try again!!!')
        elif user_input == '5':
            print('\nDelete Menu')
            print('1. Delete Bank\n2. Delete ATM\n3. Delete User Account\n4. Go back')
            user_input = input()

            if user_input == '1':
                banks, atms, users, bank_admins = delete_bank(banks, atms, users, bank_admins)
            elif user_input == '2':
                atms = update_atm_details(banks, atms, bank_admins, remove_atm=True)
            elif user_input == '3':
               users = update_user_details(banks, users, bank_admins, remove_account=True)
            elif user_input == '4':
                continue
            else:
                print('Option not valid. Try again!!!')
        elif user_input == '6':
            atms = insert_money(atms, bank_admins)
        elif user_input == '7':
            print('\nView Menu')
            print('1. Veiw all Users\n2. View User Details(only 1)\n3. Veiw all ATMs\n4. View ATM Details(only 1)\n5. Go back')
            user_input = input()

            if user_input == '1':
                view_all_users(banks, atms, users, bank_admins)
            elif user_input == '2':
                view_user_details(users)
            elif user_input == '3':
                view_all_atms(banks, atms, bank_admins)
            elif user_input == '4':
                view_atm(atms, bank_admins)
            elif user_input == '5':
                continue
            else:
                print('Option not valid. Try again!!!')
        elif user_input == '8':
            break
        else:
            print('SELECT ONE  VALID OPTION!!!')
    print("\nBye!! Come back again")



# it will have string as elements. i.e. banks = ['BOI', 'SBI', ...]
banks = []

# it will have bank name as key and its value is password
# i.e. bank_admins = {'BOI': '121', 'SBI': '1221' ....}
bank_admins = {}

# it will have list of three item as element. i.e. atms = [ ['SBI', 'Ahmedabad', 2000], ['SBI', 'Rajkot',10000],..]
atms = []

# it will have dic as value consisting of three pairs.
# i.e. users = {'BOI@5674' : {'user_name': 'parth', bank_name':'BOI', 'pin_number':'1212', 'amount':3000}, ....}
users = {}

# transcation_history = {'BOI@5674' : {'total_transaction_amount': 2000, 'total_transaction_number': 1}, ....}
transcation_history = {}

MAX_TRANSACTION = 10 # number of transactions = number of withdrawls + number of deposites
MAX_TRANSACTION_AMOUNT = 5000 # it is max amount that can be withdrawed during one day (till script exits)
INITIAL_USER_BALANCE = 1000
INITIAL_ATM_BALANCE = 100

MAIN_ADMIN_PASSWORD = '123'

run_atm(banks, atms, users, bank_admins, transcation_history, MAX_TRANSACTION, MAX_TRANSACTION_AMOUNT, INITIAL_ATM_BALANCE, INITIAL_USER_BALANCE)
