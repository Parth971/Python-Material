def is_empty(front, rear):
    return front == -1


def is_full(rear, max_size):
    return (rear + 1) == max_size


def enqueue(queue, max_size, front, rear):
    if is_full(rear, max_size):
        print("Queue is full")
    else:
        print("Enter value to be enqueued ")
        user_input = input()
        if user_input.isnumeric():
            if front == -1:
                front = 0
            rear += 1
            queue[rear] = int(user_input)
            print(f"{user_input} is enqueued successfully")
        else:
            print("Enter Numeric Value Only")

    return queue, rear, front


def dequeue(queue, front, rear):
    if is_empty(front, rear):
        print("Queue is empty")
    else:
        dequed_value = queue[front]
        queue[front] = None
        front += 1
        if front > rear:
            front = -1
            rear = -1
        print(f"Dequeued top of queue with value {dequed_value} ")

    return queue, rear, front


def peek(queue, front, rear):
    if is_empty(front, rear):
        return "Queue is empty"
    return f"Top value of queue is {queue[front]}"


def display(queue):
    print(queue)


def run_queue():
    print("Welcome to Queue")
    while True:
        max_size = input("Enter maximum size of Stack: ")

        if not max_size.isdigit():
            print("Size must be greater than 1, Enter again")
            continue

        if int(max_size) <= 0:
            print("Size must be greater than 1, Enter again")
            continue

        max_size = int(max_size)

        queue = [None] * max_size
        front = -1
        rear = -1
        while True:
            print(
                "\nEnter numbers present with operation to perform\n0. Exit Script\n1. Enqueue\n2. Dequeue\n3. Peek"
            )

            user_input = input()
            if user_input == "0":
                print("You exited Script")
                break
            elif user_input == "1":
                queue, rear, front = enqueue(queue, max_size, front, rear)
                display(queue)
            elif user_input == "2":
                queue, rear, front = dequeue(queue, front, rear)
                display(queue)
            elif user_input == "3":
                print(peek(queue, front, rear))
                display(queue)
            else:
                print("Enter Valid Input.")


run_queue()
