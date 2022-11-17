def is_empty(front, rear):
    return front == -1 and rear == -1


def is_full(front, rear, max_size):
    return (rear + 1) % max_size == front


def enqueue(queue, front, rear, max_size):
    if is_full(front, rear, max_size):
        print("Queue is full")
    else:
        print("Enter value to be enqueued ")
        user_input = input()
        if user_input.isnumeric():
            rear = (rear + 1) % max_size
            front = 0 if front == -1 else front
            queue[rear] = int(user_input)

            print(f"{user_input} is enqueued successfully")
        else:
            print("Enter Numeric Value Only")

    return queue, front, rear


def dequeue(queue, front, rear, max_size):
    if is_empty(front, rear):
        print("Queue is empty")
    else:
        if front == rear:
            dequed_value = queue[front]
            queue[front] = None
            rear = -1
            front = -1
        else:
            dequed_value = queue[front]
            queue[front] = None
            front = (front + 1) % max_size
        print(f"Dequeued top of queue with value {dequed_value}.")

    return queue, front, rear


def front_value(queue, front, rear):
    if is_empty(front, rear):
        return "Queue is empty"
    return f"Front element of circular dequeue is {queue[front]}"


def rear_value(queue, front, rear):
    if is_empty(front, rear):
        return "Queue is empty"
    return f"Rear element of circular dequeue is {queue[rear]}"


def display(queue):
    print(queue)


def run_circular_queue():
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
                "\nEnter numbers present with operation to perform\n0. Exit Script\n1. Enqueue\n2. Dequeue\n3. Front\n4. Rear"
            )

            user_input = input()
            if user_input == "0":
                print("You exited Script")
                break
            elif user_input == "1":
                queue, front, rear = enqueue(queue, front, rear, max_size)
                display(queue)
            elif user_input == "2":
                queue, front, rear = dequeue(queue, front, rear, max_size)
                display(queue)
            elif user_input == "3":
                print(front_value(queue, front, rear))
                display(queue)
            elif user_input == "4":
                print(rear_value(queue, front, rear))
                display(queue)
            else:
                print("Enter Valid Input.")


run_circular_queue()
