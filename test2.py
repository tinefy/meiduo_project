import random
import time
from multiprocessing import Process
from multiprocessing.queues import Queue

def producer(queue):
    # 把数据全部放在Queue
    for i in range(10):
        data = "这个进程id：%s， 蒸了%s个包子" % (os.getpid(), i)
        print(data)

        time.sleep(random.randint(0, 1))
        # 放入数据
        queue.put("第%s个包子" % i)


def consumer(queue):
    while True:
        res = queue.get()
        if not res: break
        data = "这个进程id：%s， 吃了%s" % (os.getpid(), res)
        print(data)


if __name__ == '__main__':
    q = Queue(3)
    p = Process(target=producer, args=(q,))
    p.start()

    p1 = Process(target=consumer, args=(q,))
    p1.start()

    # time.sleep(1000)
    # none放在这里是不行的，原因是主进程直接执行了put none, 消费者直接获取到None, 程序直接结束了
    p.join()
    q.put(None)