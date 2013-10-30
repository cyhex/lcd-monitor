__author__ = 'gx'

import time


class LoopTimer(object):


    def __init__(self, duration):

        """
        set cycle duration in seconds
        """
        self.duration = duration
        self.start = time.time()

    def wait(self):
        elapsed = time.time() - self.start
        if elapsed < self.duration:
            time.sleep(self.duration - elapsed)

        self.start = time.time()
