import os

MAX_USAGE = '85%'


class Disk(object):
    def __init__(self, path):
        self.path = path

    def get_avail_space(self):
        """
            Returns the number of available GB on the path
        """
        s = os.statvfs(self.path)
        avail_space = s.f_bsize * s.f_bavail / 1024 / 1024 / 1024
        return round(avail_space, 2)