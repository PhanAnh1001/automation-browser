# automation_multi_thread.py
from automation_one_thread import create_thread
import threading
import setting

# def main():
threadQuantity = setting.config['thread']['quantity']
accountPerThread = setting.config['thread']['accountPerThread']

thread = []
for i in range(threadQuantity):
    thread.append(threading.Thread(target=create_thread, args=(i, accountPerThread)))

for i in range(threadQuantity):
    thread[i].start()

for i in range(threadQuantity):
    thread[i].join()

# if __name__ == "__main__":
#     main()
