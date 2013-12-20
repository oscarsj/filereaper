import os
import shutil
import unittest2
import tempfile

from filereaper.executor import executor

class TestFullStack(unittest2.TestCase):

    def setUp(self):
        self.fake_path = tempfile.mkdtemp()
        self.params = {'file_owners': None, 'time_mode': 'atime',
                       'exclude_list': None, 'keep_minimum': 0,
                       'older_than_d': None, 'test_mode': False,
                       'groups_match': None, 'older_than_m': None,
                       'older_than_s': None, 'path': None,
                       'newer_than_m': None, 'remove_links': False,
                       'run_with': 'root', 'newer_than_d': None,
                       'recurse': False, 'newer_than_s': None,
                       'file_match': '.*', 'partition_size_threshold': None,
                       'file_groups': None, 'dir_size_threshold': None,
                       'keeplast': None}

    def _write_fake_file(self, filename, content):
        with open(os.path.join(self.fake_path, filename), 'w') as f:
            f.write(content)

    def tearDown(self):
        shutil.rmtree(self.fake_path)

    def test_remove_all(self):
        for i in range(10):
            self._write_fake_file('test%s' % i, 'test%scontent' % i)

        self.assertEquals(10, len(os.listdir(self.fake_path)))
        self.params['path'] = self.fake_path
        ex = executor.Executor(self.params)
        ex.execute()
        self.assertEquals(0, len(os.listdir(self.fake_path)))

    def test_file_match(self):
        for i in range(10):
            self._write_fake_file('test%s' % i, 'test%scontent' % i)

        for i in range(3):
            self._write_fake_file('other%s' % i, 'other%scontent' % i)

        self.assertEquals(13, len(os.listdir(self.fake_path)))
        self.params['path'] = self.fake_path
        self.params['file_match'] = 'other.*'
        ex = executor.Executor(self.params)
        ex.execute()
        self.assertEquals(10, len(os.listdir(self.fake_path)))

    def test_keeplast(self):
        for i in range(10):
            self._write_fake_file('test%s' % i, 'test%scontent' % i)

        self.assertEquals(10, len(os.listdir(self.fake_path)))
        self.params['path'] = self.fake_path
        self.params['keeplast'] = 2
        ex = executor.Executor(self.params)
        ex.execute()
        self.assertEquals(2, len(os.listdir(self.fake_path)))

    def test_keepminimum(self):
        for i in range(10):
            self._write_fake_file('test%s' % i, 'test%scontent' % i)

        self.assertEquals(10, len(os.listdir(self.fake_path)))
        self.params['path'] = self.fake_path
        self.params['keepminimum'] = 2
        ex = executor.Executor(self.params)
        ex.execute()
        self.assertEquals(2, len(os.listdir(self.fake_path)))

    def test_keepminimum_with_keeplast(self):
        for i in range(10):
            self._write_fake_file('test%s' % i, 'test%scontent' % i)

        self.assertEquals(10, len(os.listdir(self.fake_path)))
        self.params['path'] = self.fake_path
        self.params['keeplast'] = 2
        self.params['keepminimum'] = 3
        ex = executor.Executor(self.params)
        ex.execute()
        self.assertEquals(3, len(os.listdir(self.fake_path)))

if __name__ == '__main__':
    unittest2.main()
