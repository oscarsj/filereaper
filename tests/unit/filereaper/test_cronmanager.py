import os
import shutil
import unittest2
import tempfile

from filereaper import cronmanager, filereaper_module

class TestCronManager(unittest2.TestCase):

    fake_crons_path = None
    fake_executor = '/usr/fake/filereaper'
    fake_prefix = 'freaptest'

    def setUp(self):
        self.fake_crons_path = tempfile.mkdtemp()
        self.cronman = cronmanager.CronManager(self.fake_executor,
                                               self.fake_crons_path,
                                               self.fake_prefix)

    def tearDown(self):
        if os.path.exists(self.fake_crons_path):
            shutil.rmtree(self.fake_crons_path)

    def test_load_happy_case(self):
        fake_items = [
            ('path', '/var/log/fake'),
            ('olderthan', 5),
            ('file_match', '.*-bla'),
            ('keep_minimum', 10),
            ('test_mode', True),
            ('recursive', 'True')
        ]
        fake_module = filereaper_module.FileReaperModule('faKe fake', fake_items)
        self.cronman.load(fake_module)

        expected = """#!/bin/bash\n\n# File added by filereaper, do not change nor remove this file,\n# remove its configuration file instead and reload filereaper.\n\n/usr/fake/filereaper --path /var/log/fake --olderthan 5 --file_match .*-bla --keep_minimum 10 --test_mode --recursive """

        with open(os.path.join(self.fake_crons_path,
                               '%s_faKe_fake' % self.fake_prefix), 'r') as f:
            loaded = f.read()

        self.assertEquals(loaded, expected)

    def test_load_run_with(self):
        fake_items = [
            ('path', '/var/log/fake'),
            ('olderthan', 5),
            ('file_match', '.*-bla'),
            ('keep_minimum', 10),
            ('test_mode', True),
            ('recursive', 'True'),
            ('run_with', 'testuser')
        ]
        fake_module = filereaper_module.FileReaperModule('faKe fake', fake_items)
        self.cronman.load(fake_module)
        with open(os.path.join(self.fake_crons_path,
                               '%s_faKe_fake' % self.fake_prefix), 'r') as f:
            loaded = f.read()

        expected = """#!/bin/bash\n\n# File added by filereaper, do not change nor remove this file,\n# remove its configuration file instead and reload filereaper.\n\nsudo -u testuser sh -c \"/usr/fake/filereaper --path /var/log/fake --olderthan 5 --file_match .*-bla --keep_minimum 10 --test_mode --recursive --run_with testuser \""""

        self.assertEquals(loaded, expected)

if __name__ == '__main__':
    unittest2.main()
