import os
import shutil
import random
import copy
import tempfile
import unittest2
import time

from filereaper.executor import executor
from filereaper.executor.file_object import FileObject


class TestExecutor(unittest2.TestCase):

    fake_path = None
    fake_path_long = None
    link_dest = None

    def setUp(self):
        self.maxDiff = None
        self.fake_path = tempfile.mkdtemp()
        self.base_fake_files = ['test1.py', 'faketest2', 'test3.py', 'test4',
                                'faketest5.py']
        self.fake_files = map(lambda f: FileObject(os.path.join(self.fake_path,
                                                                f)),
                              self.base_fake_files)
        for i in self.fake_files:
            time.sleep(0.1)
            self._write_fake_file(i.path, 'test content')

    def setUpLong(self):
        self.fake_path_long = tempfile.mkdtemp()
        self.base_fake_files_long = ['test1.py', 'faketest2.py', 'test3.py',
                                     'test4', 'faketest5.py', 'faketest6.py',
                                     'faketest7.py', 'newfile.py']
        self.fake_files_long = map(lambda f: os.path.join(self.fake_path_long,
                                                          f),
                                   self.base_fake_files_long)
        for i in self.fake_files_long:
            time.sleep(0.1)
            self._write_fake_file(i, 'test content')

        # Creating subdirectories and one file per each (for the tests that
        # use recurse=True
        dirs = ['dir1', 'dir2']
        for d in dirs:
            base_dir = os.path.join(self.fake_path_long, d)
            os.mkdir(base_dir)
            time.sleep(0.1)
            self._write_fake_file(os.path.join(base_dir, 'faketest%s.py' % d),
                                  'new dir content')

        self.base_params = {
            'path': self.fake_path_long,
            'file_match': '^f.*\.py',
            'keepminimum': 1,
            'recurse': False,
            'remove_links': False,
            'exclude_list': 'faketest5.py,faketest2.py',
            'time_mode': 'ctime',
            }

    def setUpSomeSymlinks(self):
        self.link_dest = tempfile.mkdtemp()
        self.link_dest_file = os.path.join(self.link_dest, "inside_a_link.py")
        self.link_name = os.path.join(self.fake_path_long, 'faketestlink.py')
        self.link_dir_name = os.path.join(self.fake_path_long,
                                          'faketestdirlink.py')
        self._write_fake_file(self.link_dest_file, "link content")
        time.sleep(0.1)
        os.symlink(self.link_dest_file, self.link_name)
        time.sleep(0.1)
        os.symlink(self.link_dest, self.link_dir_name)

    def tearDown(self):
        if self.fake_path:
            shutil.rmtree(self.fake_path)
        if self.fake_path_long:
            shutil.rmtree(self.fake_path_long)
        if self.link_dest:
            shutil.rmtree(self.link_dest)

    def _write_fake_file(self, filename, content):
        with open(os.path.join(self.fake_path, filename), 'w') as f:
            f.write(content)

    def test__lists_intersection(self):
        """
        test__lists_intersection
        The intersection alsoa needs to preserve the source order
        """
        ex = executor.Executor({})
        list1 = ['/tmp/tmpmQFTit/faketest2.py', '/tmp/tmpmQFTit/faketest5.py',
                 '/tmp/tmpmQFTit/faketest6.py', '/tmp/tmpmQFTit/faketest7.py',
                 '/tmp/tmpmQFTit/dir1/faketestdir1.py',
                 '/tmp/tmpmQFTit/dir2/faketestdir2.py']
        list2 = ['/tmp/tmpmQFTit/faketest2.py', '/tmp/tmpmQFTit/faketest5.py',
                 '/tmp/tmpmQFTit/faketest6.py', '/tmp/tmpmQFTit/faketest7.py',
                 '/tmp/tmpmQFTit/dir1/faketestdir1.py']
        expected = ['/tmp/tmpmQFTit/faketest2.py',
                    '/tmp/tmpmQFTit/faketest5.py',
                    '/tmp/tmpmQFTit/faketest6.py',
                    '/tmp/tmpmQFTit/faketest7.py',
                    '/tmp/tmpmQFTit/dir1/faketestdir1.py']
        self.assertListEqual(expected, ex._lists_intersection(list1, list2))
        self.assertListEqual([], ex._lists_intersection(list1, []))

    def test__sort_files(self):
        ex = executor.Executor({'path': self.fake_path})
        randomized = copy.copy(self.fake_files)
        random.shuffle(randomized)
        sorted = ex._sort_files(randomized, 'ctime')
        self.assertListEqual(self.fake_files, sorted)

    def test__get_all_files_sorted(self):
        ex = executor.Executor({'path': self.fake_path})
        sorted = ex._get_all_files_sorted(self.fake_path, ".*", 'ctime',
                                          False, False)
        self.assertEqual(len(sorted), len(self.fake_files))
        sorted = ex._get_all_files_sorted(self.fake_path, "fake.*", 'ctime',
                                          False, False)
        self.assertEqual(len(sorted), 2)
        sorted = ex._get_all_files_sorted(self.fake_path, ".*\.py$", 'ctime',
                                          False, False)
        self.assertEqual(len(sorted), 3)

    def test_build_files_to_remove(self):
        """
        test_build_files_to_remove
        According to creation order (using ctime by default):
        Keeps faketest7.py and excludes faketest5.py and faketest2.py so
        only removes faketest6.py
        """
        self.setUpLong()
        ex = executor.Executor({})
        to_remove = ex._build_files_to_remove(self.base_params)
        self.assertListEqual(to_remove, map(lambda f:
                             FileObject(os.path.join(self.fake_path_long, f)),
                             ['faketest6.py']))

    def test_build_files_to_remove_with_mtime(self):
        """
        test_build_files_to_remove_with_mtime
        According to modification order (mtime), the test modifies
        faketest6.py and excludes faketest5.py and faketest2.py so
        only removes faketest7.py
        """
        self.setUpLong()
        ex = executor.Executor({})
        self.base_params['time_mode'] = 'mtime'
        self._write_fake_file(os.path.join(self.fake_path_long,
                                           'faketest6.py'),
                              'new content')
        to_remove = ex._build_files_to_remove(self.base_params)
        self.assertListEqual(to_remove, map(lambda f:
                             FileObject(os.path.join(self.fake_path_long, f)),
                             ['faketest7.py']))

    def test_build_files_to_remove_with_atime(self):
        """
        test_build_files_to_remove_with_atime
        According to access order (atime), the test reads (access)
        faketest6.py and excludes faketest5.py and faketest2.py so
        only removes faketest7.py
        """
        self.setUpLong()
        ex = executor.Executor({})
        self.base_params['time_mode'] = 'atime'
        faketest6_path = os.path.join(self.fake_path_long, 'faketest6.py')
        with open(faketest6_path, 'r') as file:
            file.read()

        to_remove = ex._build_files_to_remove(self.base_params)
        self.assertListEqual(to_remove, map(lambda f:
                             FileObject(os.path.join(self.fake_path_long, f)),
                             ['faketest7.py']))

    def test_build_files_to_remove_with_recurse(self):
        """
        test_build_files_to_remove_with_recurse
        According to creation order (ctime by default), the test creates
        two directories with a file per each and excludes faketest5.py and
        faketest2.py so, as new files have been created, removes the older
        ones that are faketest6.py, faketest7.py and dir1/faketestdir1.py
        """
        self.setUpLong()
        ex = executor.Executor({})
        self.base_params['recurse'] = True
        to_remove = ex._build_files_to_remove(self.base_params)
        expected = [
            FileObject(os.path.join(self.fake_path_long, 'faketest6.py')),
            FileObject(os.path.join(self.fake_path_long, 'faketest7.py')),
            FileObject(os.path.join(os.path.join(self.fake_path_long,
                                                 'dir1'),
                       'faketestdir1.py')),
            ]

        self.assertListEqual(to_remove, expected)

    def test_build_files_to_remove_with_recurse_depth2(self):
        """
        test_build_files_to_remove_with_recurse_depth2
        According to creation order (ctime by default), the test creates
        two directories with a file per each, two subdirs in dir1 and
        excludes faketest5.py and faketest2.py so, as new files have been
        created, removes the older ones that are faketest6.py, faketest7.py,
        dir1/faketestdir1.py, dir2/faketestdir2.py and
        dir1/subdir1/faketestsubdir1.py
        """
        self.setUpLong()
        ex = executor.Executor({})
        self.base_params['recurse'] = True
        # Creating depth 2 dirs in "dir1"
        dir1_path = os.path.join(self.fake_path_long, 'dir1')
        dirs = ['subdir1', 'subdir2']
        for d in dirs:
            base_dir = os.path.join(dir1_path, d)
            os.mkdir(base_dir)
            time.sleep(0.1)
            self._write_fake_file(os.path.join(base_dir, 'faketest%s.py' % d),
                                  'new dir content')
        to_remove = ex._build_files_to_remove(self.base_params)
        expected = [
            FileObject(os.path.join(self.fake_path_long, 'faketest6.py')),
            FileObject(os.path.join(self.fake_path_long, 'faketest7.py')),
            FileObject(os.path.join(os.path.join(self.fake_path_long,
                                                 'dir1'),
                       'faketestdir1.py')),
            FileObject(os.path.join(os.path.join(self.fake_path_long,
                                                 'dir2'),
                       'faketestdir2.py')),

            FileObject(os.path.join(os.path.join(dir1_path,
                                                 'subdir1'),
                                    'faketestsubdir1.py'))
            ]
        self.assertListEqual(to_remove, expected)

    def test_build_files_to_remove_no_remove_links(self):
        self.setUpLong()
        self.setUpSomeSymlinks()
        ex = executor.Executor({})
        self.base_params['remove_links'] = False
        # Creating a new file to have the links included in the list
        # to remove
        time.sleep(0.1)
        self._write_fake_file(os.path.join(self.fake_path_long,
                                           'faketest11.py'),
                              "fake content")
        to_remove = ex._build_files_to_remove(self.base_params)
        self.assertNotIn(FileObject(os.path.islink(self.link_name)),
                         to_remove)
        self.assertNotIn(FileObject(os.path.islink(self.link_dir_name)),
                         to_remove)

    def test_build_files_to_remove_remove_links(self):
        self.setUpLong()
        self.setUpSomeSymlinks()
        ex = executor.Executor({})
        self.base_params['remove_links'] = True
        # Creating a new file to have the links included in the list
        # to remove
        time.sleep(0.1)
        self._write_fake_file(os.path.join(self.fake_path_long,
                                           'faketest11.py'),
                              "fake content")
        to_remove = ex._build_files_to_remove(self.base_params)
        self.assertIn(FileObject(self.link_name), to_remove)
        self.assertIn(FileObject(self.link_dir_name), to_remove)

    def test_perform_removal(self):
        self.setUpLong()
        self.setUpSomeSymlinks()
        ex = executor.Executor({'test_mode': False})
        to_remove = ['faketest6.py', 'faketestdirlink.py',
                     'newfile.py', 'dir1/faketestdir1.py']
        to_remove_abs = [FileObject(os.path.join(self.fake_path_long, file))
                         for file in to_remove]
        ex._perform_removal(to_remove_abs, self.fake_path_long)
        expected = ['test3.py', 'faketestlink.py',
                    'test1.py', 'faketest2.py', 'faketest5.py',
                    'dir2', 'faketest7.py', 'test4']

        self.assertListEqual(expected, os.listdir(self.fake_path_long))
        self.assertListEqual(['faketestdir2.py'], os.listdir(os.path.join(
            self.fake_path_long, 'dir2')))

if __name__ == '__main__':
    unittest2.main()
