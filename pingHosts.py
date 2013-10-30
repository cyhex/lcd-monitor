__author__ = 'gx'
from lcdm.ping import HttpPing
from lcdm.timer import LoopTimer

hosts = [
    ('cyhex', 'http://www.cyhex.com'),
    ('autorep', 'http://www.cyhex.com'),
    ('x', 'http://www.cxxxxex.com'),
]

p = HttpPing(hosts)
timer = LoopTimer(3)

while True:

    try:
        p.ping()
        print p.hosts
        timer.wait()

    except (KeyboardInterrupt, SystemExit):
        # exit gracefully
        break