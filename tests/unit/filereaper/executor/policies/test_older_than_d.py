import os
import time
import shutil
import calendar
import unittest2
import datetime
import tempfile

import mock

from filereaper.executor.policies import older_than_d
from filereaper.executor.file_object import FileObject


class TestOlderThanD(unittest2.TestCase):

    fake_path = None
    base_params = None

    def _write_fake_file(self, filename, content):
        with open(os.path.join(self.fake_path, filename.path), 'w') as f:
            f.write(content)

    def tearDown(self):
        shutil.rmtree(self.fake_path)

    def _get_unix_timestamp(self, ndays):
        old_date = datetime.datetime.now() - datetime.timedelta(days=ndays,
                                                                hours=1,
                                                                minutes=1)
        return calendar.timegm(old_date.timetuple())

    def _prepare_files(self, newer_files, older_files):
        self.fake_files = list()
        for i, f in enumerate(older_files):
            ndays = 5 + i
            fobject = mock.MagicMock(path=f,
                                     time=self._get_unix_timestamp(ndays))
            self.fake_files.append(fobject)

        for i, f in enumerate(newer_files):
            ndays = 4 - i
            fobject = mock.MagicMock(path=f,
                                     time=self._get_unix_timestamp(ndays))
            self.fake_files.append(fobject)

        for i in self.fake_files:
            self._write_fake_file(i, 'test content')

    def setUp(self):
        self.base_params = {'file_match': '.*'}
        self.fake_path = tempfile.mkdtemp()

    def do(self, newer_files, older_files):
        self._prepare_files(newer_files, older_files)

        params = self.base_params
        params.update({'path': self.fake_path})
        policy = older_than_d.OlderThanD(5, params)
        sort = sorted(self.fake_files, key=lambda f: f.time)
        policy.set_files(sort)
        to_remove = policy.execute()
        self.assertEqual(len(older_files), len(to_remove))
        files_path = [f.path for f in to_remove]
        for f in older_files:
            self.assertIn(f, files_path)

    def test_execute(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1', 'test4', 'test3']
        newer_files = ['test2', 'test5']
        self.do(newer_files, older_files)

    def test_execute_1_file(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1']
        newer_files = []
        self.do(newer_files, older_files)

    def test_execute_1_file_bis(self):
        """
        Removing files older than 5 days
        """
        older_files = []
        newer_files = ['test3']
        self.do(newer_files, older_files)

    def test_execute_2_file(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1']
        newer_files = ['test3']
        self.do(newer_files, older_files)

    def test_execute_2_file_bis(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1', 'test3']
        newer_files = []
        self.do(newer_files, older_files)

    def test_execute_2_file_bis2(self):
        """
        Removing files older than 5 days
        """
        older_files = []
        newer_files = ['test1', 'test3']
        self.do(newer_files, older_files)

    def test_execute_3_file(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1', 'test2']
        newer_files = ['test3']
        self.do(newer_files, older_files)

    def test_execute_3_file_bis(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1', 'test3', 'test2']
        newer_files = []
        self.do(newer_files, older_files)

    def test_execute_3_file_bis2(self):
        """
        Removing files older than 5 days
        """
        older_files = []
        newer_files = ['test1', 'test3', 'test2']
        self.do(newer_files, older_files)

    def test_execute_3_file_bis3(self):
        """
        Removing files older than 5 days
        """
        older_files = ['test1']
        newer_files = ['test3', 'test2']

if __name__ == '__main__':
    unittest2.main()
