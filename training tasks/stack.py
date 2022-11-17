def is_full(top, max_size):
    return (top + 1) == max_size


def is_empty(stack, top):
    return top == -1


def push(stack, max_size, top):
    if is_full(top, max_size):
        print("Stack is full")
    else:
        print("Enter value to be pushed ")
        user_input = input()
        if user_input.isnumeric():
            top += 1
            stack += [int(user_input)]
            print(f"{user_input} is pushed successfully")
        else:
            print("Enter Numeric Value Only")

    return top


def pop(stack, top):
    if is_empty(stack, top):
        print("Stack is empty")
    else:
        poped_value = stack[top]
        stack = stack[:-1]
        top -= 1
        print(f"Poped top of stack with value {poped_value}.")

    return (top, stack)


def peep(stack, top):
    if is_empty(stack, top):
        return "Stack is empty"
    return f"Top value of stack is {stack[top]}"


def display(stack):
    print(stack)


def run_stack():
    print("Welcome to Stack")
    while True:
        max_size = input("Enter maximum size of Stack: ")

        if not max_size.isdigit():
            print("Size must be greater than 1, Enter again")
            continue

        if int(max_size) <= 0:
            print("Size must be greater than 1, Enter again")
            continue

        max_size = int(max_size)
        stack = []
        top = -1
        while True:
            print(
                "\nEnter numbers present with operation to perform\n0. Exit Script\n1. Push\n2. Pop\n3. Peep"
            )

            user_input = input()
            if user_input == "0":
                print("You exited Script")
                break
            elif user_input == "1":
                top = push(stack, max_size, top)
                display(stack)
            elif user_input == "2":
                top, stack = pop(stack, top)
                display(stack)
            elif user_input == "3":
                print(peep(stack, top))
                display(stack)
            else:
                print("Enter Valid Input.")


run_stack()
