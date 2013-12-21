import os
import time
import shutil
import unittest2
import tempfile

from filereaper.executor.policies import keepminimum


class TestKeepminimum(unittest2.TestCase):

    fake_path = None
    base_params = None

    def _write_fake_file(self, filename, content):
        with open(os.path.join(self.fake_path, filename), 'w') as f:
            f.write(content)

    def tearDown(self):
        shutil.rmtree(self.fake_path)

    def setUp(self):
        self.fake_files = ['test1', 'test2', 'test3']
        self.base_params = {'file_match': '.*'}
        self.fake_path = tempfile.mkdtemp()
        for i in self.fake_files:
            self._write_fake_file(i, 'test content')

    def test_execute(self):
        params = self.base_params
        params.update({'path': self.fake_path})
        policy = keepminimum.Keepminimum(2, params)
        policy.set_files(self.fake_files)
        to_remove = policy.execute()
        self.assertEqual(1, len(to_remove))

if __name__ == '__main__':
    unittest2.main()
