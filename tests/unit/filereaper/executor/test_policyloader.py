import os
import unittest2
import fake_policy

from filereaper.executor import policyloader


class TestPolicyLoader(unittest2.TestCase):

    fake_policy = "fake_policy"
    fake_policy_bad = "fake_policy_bad"
    fake_policy_bad2 = "fake_policy_bad2"

    def setUp(self):
        self.ploader = policyloader.PolicyLoader()
        self.ploader.BASE_MODULES = "tests.unit.filereaper.executor"

    def test_load_bad(self):
        """
        Test the import of a missing file
        """
        policy = self.ploader.load('my_fake_test', 'myvalue')
        self.assertIsNone(policy)

    def test_load_bad2(self):
        """
        Test a class with a wrong class name (it must be the file name
        camel cased)
        """
        policy = self.ploader.load(self.fake_policy_bad, 'myvalue')
        self.assertIsNone(policy)

    def test_load_bad3(self):
        """
        Test the import of a class with a wrong __init__() method
        """
        policy = self.ploader.load(self.fake_policy_bad2, 'myvalue')
        self.assertIsNone(policy)

    def test_load_good(self):
        """
        Import a good policy
        """
        policy = self.ploader.load(self.fake_policy, 'myvalue')
        self.assertIsInstance(policy, fake_policy.FakePolicy)

if __name__ == '__main__':
    unittest2.main()
