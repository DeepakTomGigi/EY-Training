import threading
import queue
import time
import random

# Shared queue
q = queue.Queue()

def producer():
    for i in range(5):
        item = f"Item-{i}"
        q.put(item)
        print(f"Produced: {item}")
        time.sleep(random.uniform(0.5, 1.5))  # simulate variable work

def consumer():
    while True:
        item = q.get()
        if item is None:  # signal to stop
            break
        print(f"Consumed: {item}")
        time.sleep(random.uniform(1, 2))
        q.task_done()

# Create threads
prod_thread = threading.Thread(target=producer)
cons_thread = threading.Thread(target=consumer)

prod_thread.start()
cons_thread.start()

prod_thread.join()
q.put(None)  # stop signal
cons_thread.join()
