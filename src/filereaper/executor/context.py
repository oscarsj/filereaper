"""
Implements the context in the strategy pattern
"""
class Context(object):

    def __init__(self, policy):
        self.policy = policy

    def execute_policy(self):
        return self.policy.execute()
