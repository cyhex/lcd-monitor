__author__ = 'gx'
from interface import RenderInterface
from lcdm.ping import HostEntity


class RenderConsole(RenderInterface):
    """
    render host to console (stdOut)
    """
    def render(self):
        print self.hosts
