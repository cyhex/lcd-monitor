__author__ = 'gx'
from lcdm.ping import HttpPing
from lcdm.timer import LoopTimer

hosts = [
    {'name': 'cyhex', 'url': 'http://www.cyhex.com'},
    {'name': 'autorep', 'url': 'http://www.autoreparaturen.de'}
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