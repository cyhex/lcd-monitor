__author__ = 'gx'

import requests
import time
import threading
import Queue

class HostEntity(object):

    # simple moving average size
    SMA_SIZE = 10

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.times = []
        # Time
        self.offline_since = 0

    def get_last_time(self):
        return self.times[-1:][0]

    def get_avg_time(self):

        #cut times tail above SMA_SIZE
        if len(self.times) > self.SMA_SIZE:
            self.times = self.times[self.SMA_SIZE*-1:]

        return sum(self.times)/len(self.times)

    def set_offline(self):
        if self.offline_since == 0:
            self.offline_since = time.time()

    def get_offline_since(self):
        return time.time() - self.offline_since

    def set_online(self):
        self.offline_since = 0

    def is_online(self):
        return self.offline_since == 0

    def __repr__(self):
        if self.is_online():
            return "%s: %0.3fs %0.3fs" % (self.name, self.get_last_time(), self.get_avg_time())
        else:
            return "%s: offline since  %0.3fs" % (self.name, self.get_offline_since())


class HttpPingWorker(threading.Thread):

    # in seconds
    DEFAULT_TIMEOUT = 3

    def __init__(self, queue):
        """
        Gets HostEntity from hosts_queue_in - calculates ping time

        :type queue: Queue.Queue
        """
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            h = self.queue.get()
            assert isinstance(h, HostEntity)
            try:
                r = requests.get(h.url, timeout=self.DEFAULT_TIMEOUT)
                h.times.append(r.elapsed.total_seconds())
                h.set_online()
            except:
                h.set_offline()

            self.queue.task_done()

class HttpPingWorkerPool(object):

    def __init__(self, pool_size):
        """
        Just a pool manager for HttpPingWorker
        No work is been done at this point
        """
        self.workers = []
        self.queue = Queue.Queue()

        # create one thread per host
        for i in range(pool_size):
            t = HttpPingWorker(self.queue)
            t.setDaemon(True)
            t.start()

            self.workers.append(t)

    def put(self, hosts):
        """
        start doing work as soon as queue is populated
        """
        for host in hosts:
            self.queue.put(host)

    def wait(self):
        """
        wait till all queue is empty
        """
        self.queue.join()
