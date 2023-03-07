import hazelcast
from threading import Thread
from time import sleep

def produce():
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    for i in range(100):
        queue.offer(i)
        print("Producing" + str(i))
        #sleep(1)
    print("Producing is finished!")
    client.shutdown()

def consume(consumer, con_finished):
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    consumed_count = 0

    while consumed_count < 50:
        head = queue.take().result()
        print(consumer + " consuming {}".format(head))
        consumed_count += 1
    print(con_finished)
    client.shutdown()

producer_thread = Thread(target=produce)
consumer1_thread = Thread(target=consume, args=("Consumer1", "Consumer1 has finished his work"))
consumer2_thread = Thread(target=consume, args=("Consumer2", "Consumer2 has finished his work"))

producer_thread.start()
consumer1_thread.start()
consumer2_thread.start()

