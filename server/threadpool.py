from concurrent.futures import ThreadPoolExecutor
import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:9000")


def task(i):
    print(proxy.get_topic('ciao' + str(i)))
    return i


executor = ThreadPoolExecutor(10)
for i in range(0,10):
    future = executor.submit(task, i)
    if future.done() is not False:
        print(future.done())
