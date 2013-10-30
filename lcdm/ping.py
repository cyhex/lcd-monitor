__author__ = 'gx'

import requests
import time


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


class HttpPing(object):

    # in seconds
    DEFAULT_TIMEOUT = 3

    def __init__(self, hosts):
        """
        Hosts:list of tupels [(host_name, url)]
        """
        self.hosts = []

        for h in hosts:
            self.hosts.append(HostEntity(*h))

    def ping(self):

        for h in self.hosts:
            try:
                r = requests.get(h.url, timeout=self.DEFAULT_TIMEOUT)
                h.times.append(r.elapsed.total_seconds())
                h.set_online()
            except:
                h.set_offline()
