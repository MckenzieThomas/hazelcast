import hazelcast
from threading import Thread
from time import sleep

def insert_into_map(key, last_message):
    client = hazelcast.HazelcastClient()
    my_map = client.get_map("my-distributed-map").blocking()
    my_map.put(key, 0)
    print("Starting")
    for x in range(1000):
        while(True):
            old_value = my_map.get(key)
            new_value = old_value + 1
            if(my_map.replace_if_same(key, old_value, new_value)):
                break
    print(last_message, my_map.get(key))
    client.shutdown()

key = "oploc"
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