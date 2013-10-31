__author__ = 'gx'

class RenderInterface(object):

    def __init__(self, hosts):
        self.hosts = hosts

    def render(self):
        for host in self.hosts:
            self._renderHost(host)

    def _renderHost(self, host):
        pass