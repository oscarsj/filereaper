import os
import unittest2
import tempfile

from filereaper import filereaper_module


class TestFileReaperModule(unittest2.TestCase):

    def test_attributes(self):
        fake_items = [
            ('path', '/var/log/fake'),
            ('olderthan', 5),
            ('file_match', '.*-bla'),
            ('keep_minimum', 10),
        ]
        fake_module = filereaper_module.FileReaperModule('fake', fake_items)
        self.assertListEqual(['path', 'olderthan', 'file_match',
                              'keep_minimum'],
                             fake_module.attributes)

if __name__ == '__main__':
    unittest2.main()
