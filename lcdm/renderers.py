__author__ = 'gx'
"""
@todo: if the file get bigger - refactor renderer per file

"""

from lcdm.ping import HostEntity
from lcdm.pylcdsysinfo import LCDSysInfo, BackgroundColours, TextColours, TextLines, TextAlignment

class RenderInterface(object):

    def __init__(self, hosts):
        self.hosts = hosts

    def render(self):
        for host in self.hosts:
            self.render_host(host)

    def render_host(self, host):
        pass


class RenderConsole(RenderInterface):
    """
    render host to console (stdOut)
    """
    def render(self):
        print self.hosts


class RenderLcd6Rows(RenderInterface):
    """
    render host to lcd in 6 rows
    """
    def __init__(self, hosts):
        super(RenderLcd6Rows, self).__init__(hosts)

        self.lcd = LCDSysInfo()
        self.lcd.set_text_background_colour(BackgroundColours.BLACK)
        self.lcd.set_brightness(255)
        self.lcd.dim_when_idle(False)
        self.lcd.clear_lines(TextLines.ALL, BackgroundColours.BLACK)
        self.lcd.display_text_on_line(TextLines.LINE_1, 'Host\tLast/Avg (s)', pad_for_icon=False, alignment=TextAlignment.LEFT, colour=TextColours.GREY)

    def render_host(self, host):
        assert isinstance(host, HostEntity)
        line = self.get_line(host)

        #self.lcd.clear_lines(line, BackgroundColours.BLACK)

        if not host.is_online():
            color = TextColours.RED
            text = "%s\t%0.3f" % (host.name, host.get_offline_since())
        else:
            color = TextColours.GREEN
            text = "%s\t%0.3f/%0.3f" % (host.name, host.get_last_time(), host.get_avg_time())


        self.lcd.display_text_on_line(line, text, pad_for_icon=False, alignment=TextAlignment.LEFT, colour=color)

    def get_line(self, host):
        return self.hosts.index(host) + 2