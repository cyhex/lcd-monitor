__author__ = 'gx'

import requests


class HostEntity(object):
    """
    Represents a host to ping
    """

    # simple moving response times average
    SMA_SIZE = 10

    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.times = []

    def get_last_time(self):
        return self.times[-1:][0]

    def get_avg_time(self):
        #cut times tail above SMA_SIZE
        if len(self.times) > self.SMA_SIZE:
            self.times = self.times[self.SMA_SIZE*-1:]

        return sum(self.times)/len(self.times)

    def is_online(self):
        return self.get_last_time() != -1

    def __repr__(self):
        return "%s: %0.3fs %0.3fs" % (self.name, self.get_last_time(), self.get_avg_time())


class HttpPing(object):

    # in seconds
    DEFAULT_TIMEOUT = 3

    def __init__(self, hosts):
        self.hosts = []

        for h in hosts:
            he = HostEntity(h['name'], h['url'])
            self.hosts.append(he)

    def ping(self):

        for h in self.hosts:
            try:
                r = requests.get(h.url, timeout=self.DEFAULT_TIMEOUT)
                h.times.append(r.elapsed.total_seconds())
            except requests.Timeout:
                h.times.append(-1)
