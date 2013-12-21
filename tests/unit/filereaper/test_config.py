import os
import unittest2
import tempfile

from ConfigParser import ConfigParser

from filereaper.config import Config


class TestConfig(unittest2.TestCase):

    good_fake_file_content = """[my section!]
myvar=10
othervar='is a string'
oneboolean=True
"""

    bad_fake_file_content1 = """
myvar=10
othervar='is a string'
oneboolean=True
"""
    bad_fake_file_content2 = """[my section!]
myvar=10
othervar='is a string'
oneboolean
"""

    tempfile = ''

    def setUp(self):
        self.tempfile = tempfile.mkstemp()[1]

    def tearDown(self):
        if os.path.exists(self.tempfile):
            os.remove(self.tempfile)

    def test_get_module_ok(self):
        with open(self.tempfile, 'w') as f:
            f.write(self.good_fake_file_content)
        config = Config(self.tempfile)
        module = config.get_module()
        self.assertEquals(module.name, "my section!")
        self.assertIsInstance(module.myvar, int)
        self.assertIsInstance(module.oneboolean, bool)
        self.assertIsInstance(module.othervar, str)

    def test_get_module_bad1(self):
        with open(self.tempfile, 'w') as f:
            f.write(self.bad_fake_file_content1)
        config = Config(self.tempfile)
        module = config.get_module()
        self.assertIsNone(module)

    def test_get_module_bad2(self):
        with open(self.tempfile, 'w') as f:
            f.write(self.bad_fake_file_content2)
        config = Config(self.tempfile)
        module = config.get_module()
        self.assertIsNone(module)

    def test_get_module_bad3(self):
        config = Config('/does/not/exist')
        module = config.get_module()
        self.assertIsNone(module)


if __name__ == '__main__':
    unittest2.main()
