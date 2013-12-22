import datetime

from older_than_base import OlderThanBase


class OlderThanM(OlderThanBase):

    def get_thetime(self, older_than_m):
        return datetime.datetime.now() - datetime.timedelta(
            minutes=older_than_m)
