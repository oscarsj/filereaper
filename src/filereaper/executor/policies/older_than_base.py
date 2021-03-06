import os
import datetime

from base_policy import BasePolicy


class OlderThanBase(BasePolicy):

    def get_thetime(self):
        raise NotImplemented("To be implemented in subclasses")

    def execute(self):
        path = self.params['path']
        thetime = self.get_thetime(self.value)

        # Binary search adapted to find the items around "thetime"
        size = len(self.sorted_files)
        if size == 0:
            return list()
        index = self._binary_search(0, size-1, thetime, self.sorted_files)
        return self.sorted_files[:index]

    def _binary_search(self, first, last, thetime, files):
        if last == first:
            if datetime.datetime.fromtimestamp(files[first].time) <= thetime:
                return first + 1
            else:
                if first - 1 < 0:
                    return 0
                else:
                    return first

        middle = int((last+first)/2)
        middle_datetime = datetime.datetime.fromtimestamp(files[middle].time)
        if middle_datetime >= thetime:
            return self._binary_search(first, middle, thetime, files)
        else:
            return self._binary_search(middle+1, last, thetime, files)
