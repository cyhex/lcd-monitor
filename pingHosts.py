from duplicity.tarfile import _hole

__author__ = 'gx'
from lcdm.ping import HttpPingThreaded, HostEntity
from lcdm.timer import LoopTimer
from lcdm.pylcdsysinfo import LCDSysInfo, BackgroundColours, TextColours, TextLines
import Queue

hosts = [
    ('cyhex', 'http://www.cyhex.com'),
    ('autorep', 'http://www.cyhex.com'),
    ('x', 'http://www.cxxxxex.com'),
]



class DrawHosts(object):
    # main loop update time in seconds
    CYCLE_TIME = 3

    def __init__(self):
        self.timer = LoopTimer(self.CYCLE_TIME)
        self.run_flag = True
        self.host_queue = Queue.Queue()
        self.hosts = [HostEntity(*h) for h in hosts]

        #self.lcd = LCDSysInfo()
        #self.lcd.set_text_background_colour(BackgroundColours.BLACK)
        #self.lcd.set_brightness(255)
        #self.lcd.dim_when_idle(False)

    def run(self):
        while self.run_flag:

            # create one thread per host
            for i in range(len(self.hosts)):
                t = HttpPingThreaded(self.host_queue)
                t.setDaemon(True)
                t.start()

            for host in self.hosts:
                self.host_queue.put(host)

            # wait until all threads are done
            self.host_queue.join()

            print self.hosts

            # make sure we do not flood the servers...
            self.timer.wait()




d = DrawHosts()
try:
    d.run()
except (KeyboardInterrupt, SystemExit):
    d.run_flag = False;