
__author__ = 'gx'
from lcdm.ping import HostEntity, HttpPingWorkerPool
from lcdm.timer import LoopTimer
from lcdm.pylcdsysinfo import LCDSysInfo, BackgroundColours, TextColours, TextLines

hosts = [
    ('cyhex', 'http://www.cyhex.com'),
    ('autorep', 'http://www.autoreparaturen.de'),
    ('x', 'http://www.cxxxxex.com'),
]


class DrawHosts(object):
    # main loop update time in seconds
    CYCLE_TIME = 3

    def __init__(self):
        self.timer = LoopTimer(self.CYCLE_TIME)
        self.run_flag = True
        self.hosts = [HostEntity(*h) for h in hosts]
        self.pool = HttpPingWorkerPool(len(self.hosts))
        #self.lcd = LCDSysInfo()
        #self.lcd.set_text_background_colour(BackgroundColours.BLACK)
        #self.lcd.set_brightness(255)
        #self.lcd.dim_when_idle(False)

    def run(self):
        while self.run_flag:
            # put jobs to ping
            self.pool.put(self.hosts)
            # wait till done
            self.pool.wait()

            print self.hosts

            # independent loop timer
            self.timer.wait()


d = DrawHosts()
try:
    d.run()
except (KeyboardInterrupt, SystemExit):
    d.run_flag = False;