import hazelcast
from threading import Thread
from time import sleep

def insert_into_map(key, last_message):
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("my-distributed-map").blocking()
    my_map.put(key, 0)
    print("Starting")
    for x in range(1000):
        my_map.lock(key)
        try:
            value = my_map.get(key)
            value += 1
            my_map.put(key, value)
        finally:
            my_map.unlock(key)
    print(last_message, my_map.get(key))
    client.shutdown()

key = "pemloc"
thread = Thread(target=insert_into_map, args=(key, "Thread number one has finished his work. Result = "))
thread2 = Thread(target=insert_into_map, args=(key, "Thread number two has finished his work. Result = "))
thread3 = Thread(target=insert_into_map, args=(key, "Thread number three has finished his work. Result = "))
thread.start()
thread2.start()
thread3.start()

sleep(5)
client = hazelcast.HazelcastClient()
my_map = client.get_map("my-distributed-map").blocking()
print("Finished! Result = ", my_map.get(key))
client.shutdown()