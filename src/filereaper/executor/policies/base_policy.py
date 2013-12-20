"""
Base class. All policies must extends from this class
"""

class BasePolicy(object):

    value = None
    params = None
    sorted_files = None

    def __init__(self, value, params):
        self.value = value
        self.params = params
        self.sorted_files = None

    def set_files(self, files):
        self.sorted_files = files

    def execute(self):
        #TODO use custom exception instead
        raise NotImplemented("To be implemented in subclass")
