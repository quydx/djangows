import os

MAX_USAGE = '85%'


class Disk(object):
    def __init__(self):
        pass

    def get_avail_space(self, path):
        """
            Returns the number of available GB on the path
        """
        s = os.statvfs(path)
        avail_space = s.f_bsize * s.f_bavail / 1024 / 1024 / 1024
        return round(avail_space, 2)