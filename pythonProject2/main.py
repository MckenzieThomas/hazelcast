import hazelcast

client = hazelcast.HazelcastClient()
my_map = client.get_map("my-distributed-map").blocking()
for x in range(1000):
    my_map.put("key " + str(x), x)
    print(x)
client.shutdown()


