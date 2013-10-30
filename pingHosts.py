from duplicity.tarfile import _hole

__author__ = 'gx'
from lcdm.ping import HttpPing, HostEntity
from lcdm.timer import LoopTimer
from lcdm.pylcdsysinfo import LCDSysInfo, BackgroundColours, TextColours

hosts = [
    ('cyhex', 'http://www.cyhex.com'),
    ('autorep', 'http://www.cyhex.com'),
    ('x', 'http://www.cxxxxex.com'),
]



class DrawHosts(object):

    def __init__(self):
        self.ping = HttpPing(hosts)
        self.timer = LoopTimer(3)
        self.run_flag = True
        self.lcd = LCDSysInfo()
        self.lcd.set_text_background_colour(BackgroundColours.BLACK)
        self.lcd.set_brightness(255)
        self.lcd.dim_when_idle(False)

    def draw(self, line, host):
        assert isinstance(host, HostEntity)

        color = TextColours.GREEN

        if not host.is_online():
            color = TextColours.RED

        self.lcd.display_text_on_line(line, host.get_lcd_formatted(), colour=color)

    def run(self):

        while self.run_flag:
            self.ping.ping()
            print self.ping.hosts
            self.timer.wait()



d = DrawHosts()
try:
    d.run()
except (KeyboardInterrupt, SystemExit):
    d.run_flag = False;