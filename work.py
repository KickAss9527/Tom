import threading, queue, time

class Work(threading.Thread):
    def __init__(self, work_queue):
        self.work_queue = work_queue
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        while True:
            try:
                if self.work_queue.empty():
                    time.sleep(1)
                    print('sleep over')
                    continue;
                items = self.work_queue.get(block=False)
                fun = items[0]
                args = items[1]
                fun(args)
                self.work_queue.task_done()
                print('left work count : ', self.work_queue.qsize())
            except Exception as e:
                print('ex:',e)
                break;