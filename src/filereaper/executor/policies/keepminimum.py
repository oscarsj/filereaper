from base_policy import BasePolicy


class Keepminimum(BasePolicy):

    def execute(self):
        """
        """
        path = self.params['path']
        keepminimum = self.value
        return self.sorted_files[:len(self.sorted_files)-keepminimum]
