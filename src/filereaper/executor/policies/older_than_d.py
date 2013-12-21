import os

from base_policy import BasePolicy


class Keeplast(BasePolicy):

    def execute(self):
        path = self.params['path']
        older_than_d = self.value
        return self.sorted_files[:len(self.sorted_files)-keeplast]
