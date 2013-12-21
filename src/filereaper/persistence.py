import sqlite3
import hashlib


class Persistence(object):

    TABLE_NAME = 'filereapermodules'

    _conn = None
    persistence_file = None

    @property
    def conn(self):
        if not self._conn:
            self._conn = sqlite3.connect(self.persistence_file)
        return self._conn

    @property
    def cursor(self):
        return self.conn.cursor()

    def __init__(self, persistence_file):
        self.persistence_file = persistence_file

    def store(self, module):
        md5 = hashlib.md5(open(module).read()).hexdigest()
        self._store(module, md5)

    def clean(self, modules):
        deleted = list()
        current_ids = self._get_ids()
        for mod in modules:
            md5 = hashlib.md5(open(mod).read()).hexdigest()
            if md5 in current_ids:
                current_ids.remove(md5)

        for deleted_id in current_ids:
            name = self._get_name(deleted_id)
            if name:
                deleted.append(self._get_name(deleted_id))
                self._delete(deleted_id)

        return deleted

    def filter_old(self, modules):
        filtered = list()
        current_ids = self._get_ids()
        for mod in modules:
            md5 = hashlib.md5(open(mod).read()).hexdigest()
            if not md5 in current_ids:
                filtered.append(mod)
        return filtered

    def _store(self, module, md5):
        try:
            self.cursor.execute('insert into %s values (?, ?)'
                                % self.TABLE_NAME,
                                (md5, module))
        except sqlite3.OperationalError:
            self._create_table()
            return self._store(module, md5)

    def _get_name(self, id):
        try:
            return self.cursor.execute('select name from %s where id=?'
                                       % self.TABLE_NAME,
                                       (id,)).fetchone()[0]
        except sqlite3.OperationalError:
            return None

    def _delete(self, id):
        try:
            self.cursor.execute('delete from %s where id=?' % self.TABLE_NAME,
                                (id,))
        except sqlite3.OperationalError:
            pass

    def _get_ids(self):
        try:
            rows = self.cursor.execute('select id from %s'
                                       % self.TABLE_NAME).fetchall()
            return [row[0] for row in rows]
        except sqlite3.OperationalError:
            self._create_table()
            return self._get_all()

    def _create_table(self):
        self.cursor.execute('create table %s (id text, name text)'
                            % self.TABLE_NAME)
