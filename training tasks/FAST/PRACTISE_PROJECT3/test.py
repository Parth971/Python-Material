# from contextlib import suppress
#
# BaseSuppressException = suppress
#
# class TT(BaseSuppressException):
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if x := super().__exit__(exc_type, exc_val, exc_tb):
#             return x
#
#
# with TT(NameError):
#     raise NameError('KKKKKKKK')
# import sys
#
# z = 'ffff'
# parth = 'parth'
#
# print(getattr(sys.modules[__name__], ))
#
# import multiprocessing
# import time
#
# import requests
#
#
# def square_numbers(count):
#     print("started for", count, time.time()-s)
#     response = requests.get('http://127.0.0.1:8000/users/me')
#     print(f"Square of {count}: ", response.status_code)
#
#
# if __name__ == '__main__':
#     # Define the list of numbers to square
#     numbers = list(range(500))
#     s = time.time()
#     # Create a process pool with four worker processes
#     pool = multiprocessing.Pool(processes=len(numbers))
#
#     # Use the process pool to asynchronously execute the square_numbers function
#     # on each number in the list
#     pool.map(square_numbers, numbers)
#     print("Done")
#     # Close the process pool to free resources
#     pool.close()
#     # pool.join()
#     print("Closed")
# import time
#
# import requests
# import multiprocessing
#
# # Define the function to be executed in each process
# def send_request(url):
#     requests.get(url)
#
# # Define the list of URLs to be requested
# urls = ["http://127.0.0.1:8000/users/me"] * 500
#
# # Create a list to hold the processes
# processes = []
# s = time.time()
# # Start each process to send a request
# for url in urls:
#     p = multiprocessing.Process(target=send_request, args=(url,))
#     processes.append(p)
#     p.start()
# print(time.time()-s)
#
# # Wait for all processes to complete
# for p in processes:
#     p.join()

import asyncio
import time

import aiohttp

# Define the coroutine to send requests
async def send_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            pass

# Define the list of URLs to be requested
urls = ["http://127.0.0.1:8000/users/me"] * 500

# Create a coroutine to run all requests concurrently
async def send_requests():
    tasks = []
    s = time.time()
    for url in urls:
        task = asyncio.create_task(send_request(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(time.time()-s)

s = time.time()
# Run the coroutine to send the requests
asyncio.run(send_requests())
print(time.time()-s)
