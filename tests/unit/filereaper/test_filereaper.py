import os
import unittest2
import tempfile

from mock import MagicMock, patch

from filereaper import filereaper, config, persistence, cronmanager


class TestFileReaper(unittest2.TestCase):

    fake_crons_path = None
    fake_modules_dir = '/fake/dir'
    fake_main_config_file = 'test'

    def setUp(self):
        self.fake_crons_path = tempfile.mkdtemp()

    def tearDown(self):
        pass

    @unittest2.skip("not working yet")
    def test_run_bad1(self, mock_class):
        mock_class.get_module.return_value = True
        freaper = filereaper.FileReaper(self.fake_modules_dir,
                                        self.fake_main_config_file)
        self.assertFalse(freaper.run())

    @unittest2.skip("not working yet")
    def test_run(self):
        return True
        """
        In this test the module3 is added and module0 was removed
        """
        fs_modules = ['module1', 'module2', 'module3']
        new_modules = ['module3']
        old_modules = ['module1', 'module2']
        delete_modules = ['module0']

        with patch.object(filereaper.FileReaper,
                          '_get_modules_configs',
                          return_value=fs_modules):
            fake_config = config.Config(self.fake_main_config_file)
            fake_config.get_module = MagicMock(return_value=True)

            fake_pers = persistence.Persistence('/path/file.db')
            fake_pers.filter_old = MagicMock(return_value=new_modules)

            fake_pers.clean = MagicMock()
            fake_pers.clean(return_value=delete_modules)
            fake_pers.store = MagicMock()

            fake_config_delete = config.Config('module0')
            fake_config_delete.get_module = MagicMock(
                return_value='module0real')

            fake_cronman = cronmanager.CronManager('fake', 'fake', 'fake')
            fake_cronman.delete = MagicMock()

            fake_cronman.load = MagicMock()

            fake_config_new = config.Config('module3')
            fake_config_new.get_module = MagicMock(return_value='module3real')

            freaper = filereaper.FileReaper(self.fake_modules_dir,
                                            self.fake_main_config_file)
            freaper.run()

            fake_pers.filter_old.assert_called_once_with(fs_modules)
            fake_pers.store.assert_called_once_with('module3real')
            fake_cronman.delete.assert_called_once_with('module0real')
            fake_cronman.load.assert_called_once_with('module3real')

if __name__ == '__main__':
    unittest2.main()
