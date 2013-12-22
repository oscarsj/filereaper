import datetime

from older_than_base import OlderThanBase


class OlderThanS(OlderThanBase):

    def get_thetime(self, older_than_s):
        return datetime.datetime.now() - datetime.timedelta(
            seconds=older_than_s)
