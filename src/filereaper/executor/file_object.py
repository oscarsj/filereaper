from collections import namedtuple


class FileObject(object):

    path = None
    time = None

    def __init__(self, path, time=None):
        self.path = path
        self.time = time

    def __eq__(self, other):
        return self.path == other.path

    def __str__(self):
        return self.path
