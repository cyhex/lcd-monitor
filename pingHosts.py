# !/usr/bin/env python
__author__ = 'gx'
from lcdm.ping import HostEntity, HttpPingWorkerPool
from lcdm.timer import LoopTimer
from lcdm.renderers import RenderLcd6Rows, RenderConsole

hosts = [
    ('cyhex', 'http://www.cyhex.com'),
    ('Autorep', 'http://www.autoreparaturen.de'),
    ('Blog', 'http://blog.autoreparaturen.de'),
    ('Markt', 'http://autoteile-markt.de'),
]

class DrawHosts(object):
    # main loop update time in seconds
    CYCLE_TIME = 5

    def __init__(self):
        self.timer = LoopTimer(self.CYCLE_TIME)
        self.run_flag = True
        self.hosts = [HostEntity(*h) for h in hosts]
        # one thread per host
        self.pool = HttpPingWorkerPool(len(self.hosts))

        #RenderLcd6Rows(self.hosts)
        self.renderers = [
            # RenderConsole(self.hosts),
            RenderLcd6Rows(self.hosts)
        ]

    def run(self):
        while self.run_flag:
            self.pool.put(self.hosts)
            self.pool.wait()
            [r.render() for r in self.renderers]

            # independent loop timer
            self.timer.wait()

d = DrawHosts()
try:
    d.run()
except (KeyboardInterrupt, SystemExit):
    d.run_flag = False
