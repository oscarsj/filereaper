import datetime

from older_than_base import OlderThanBase


class OlderThanD(OlderThanBase):

    def get_thetime(self, older_than_d):
        return datetime.datetime.now() - datetime.timedelta(
            days=older_than_d)
