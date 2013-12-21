import os
import unittest2
import tempfile

from filereaper import persistence


class TestPersistence(unittest2.TestCase):

    pers = None
    pers_file = None
    temp1 = ''
    temp2 = ''

    def setUp(self):
        self.pers_file = tempfile.mkstemp()[1]
        self.pers = persistence.Persistence(self.pers_file)

    def tearDown(self):
        if os.path.exists(self.pers_file):
            os.remove(self.pers_file)
        if os.path.exists(self.temp1):
            os.remove(self.temp1)
        if os.path.exists(self.temp2):
            os.remove(self.temp2)

    def _create_files(self):
        self.temp1 = tempfile.mkstemp()[1]
        self.temp2 = tempfile.mkstemp()[1]
        with open(self.temp1, 'w') as f:
            f.write("first content")
        with open(self.temp2, 'w') as f:
            f.write("file content")

    def _load_some_fixtures(self):
        self._create_files()

        self.BASIC_FIXTURES = [
            # md5 hash of: "first content"
            ('129a8c30e1c3ad89d2635f8abdfdb50b', self.temp1),
            # md5 hash of: "file content"
            ('d10b4c3ff123b26dc068d43a8bef2d23', self.temp2),
            ('ccccaaa', 'test3'),
            ('1234567', 'test4'),
        ]

        cursor = self.pers.conn.cursor()
        cursor.execute('create table %s (id text, name text)'
                       % self.pers.TABLE_NAME)
        cursor.executemany('insert into %s values (?, ?)'
                           % self.pers.TABLE_NAME, self.BASIC_FIXTURES)

    def test_filter_old(self):
        """
        Let's suppose temp1 and temp2 were already used
        """
        self._load_some_fixtures()
        new_module = tempfile.mkstemp()[1]
        all_mods = [self.temp1,
                    self.temp2,
                    new_module]

        filtered = self.pers.filter_old(all_mods)
        self.assertEquals([new_module],
                          filtered)
        os.remove(new_module)

    def test_store(self):
        self._create_files()
        self.pers.store(self.temp1)
        self.pers.store(self.temp2)

        cursor = self.pers.conn.cursor()
        modules = cursor.execute('select name from %s'
                                 % self.pers.TABLE_NAME).fetchall()
        modules = [mod[0] for mod in modules]
        self.assertEquals([self.temp1, self.temp2], modules)

    def test_clean(self):
        """
        temp1, test3 and test4 were removed so must be cleaned
        """
        self._load_some_fixtures()
        deleted = self.pers.clean([self.temp1])
        removed = self.BASIC_FIXTURES
        removed.remove(('129a8c30e1c3ad89d2635f8abdfdb50b', self.temp1))
        self.assertEquals(deleted, [rem[1] for rem in removed])
        cursor = self.pers.conn.cursor()
        data = cursor.execute('select name from %s'
                              % self.pers.TABLE_NAME).fetchall()
        self.assertEquals(self.temp1, data[0][0])

if __name__ == '__main__':
    unittest2.main()
