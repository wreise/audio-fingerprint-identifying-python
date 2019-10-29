from .db import Database
from .config import get_config
import sqlite3
import sys
from itertools import zip_longest
from termcolor import colored

class SqliteDatabase(Database):
    TABLE_SONGS = 'songs'
    TABLE_FINGERPRINTS = 'fingerprints'

    def __init__(self):
        self.connect()

    def connect(self):
        config = get_config()

        self.conn = sqlite3.connect(config['db.file'])
        self.conn.text_factory = str

        self.cur = self.conn.cursor()

        print(colored('sqlite - connection opened','white',attrs=['dark']))

    def __del__(self):
        self.conn.commit()
        self.conn.close()
        print(colored('sqlite - connection has been closed','white',attrs=['dark']))

    def query(self, query, values = []):
        self.cur.execute(query, values)

    def executeOne(self, query, values = []):
        self.cur.execute(query, values)
        return self.cur.fetchone()

    def executeAll(self, query, values = []):
        self.cur.execute(query, values)
        return self.cur.fetchall()

    def buildSelectQuery(self, table, params):
        conditions = []
        values = []

        for k, v in enumerate(params):
            key = v
            value = params[v]
            conditions.append("%s = ?" % key)
            values.append(value)

        conditions = ' AND '.join(conditions)
        query = "SELECT * FROM %s WHERE %s" % (table, conditions)
        return { "query": query, "values": values }

    def findOne(self, table, params):
        select = self.buildSelectQuery(table, params)
        return self.executeOne(select['query'], select['values'])

    def findAll(self, table, params):
        select = self.buildSelectQuery(table, params)
        return self.executeAll(select['query'], select['values'])

    def insert(self, table, params):
        keys = ', '.join(params.keys())
        values = params.values()
        nb_params = len(params)
        query = "INSERT INTO %s (%s) VALUES (%s)" % (table, keys, ','.join(["?"]*nb_params))

        self.cur.execute(query, tuple(values))
        self.conn.commit()

        return self.cur.lastrowid

    def insertMany(self, table, columns, values):
        query = "INSERT OR IGNORE INTO %s (%s) VALUES (%s)" % (table, ", ".join(columns), ", ".join(["?"]*len(columns)))
        self.cur.executemany(query, values)
        self.conn.commit()

    def get_song_hashes_count(self, song_id):
        query = 'SELECT count(*) FROM %s WHERE song_fk = %d' % (self.TABLE_FINGERPRINTS, song_id)
        rows = self.executeOne(query)
        return int(rows[0])

    def return_matches(self, hashes):
        def grouper(iterable, n, fillvalue=None):
            args = [iter(iterable)] * n
            return [list(filter(None, values)) for values
                in zip_longest(fillvalue=fillvalue, *args)]
        mapper = {}
        for hash, offset in hashes:
            mapper[hash.upper()] = offset
        values = mapper.keys()

        for split_values in grouper(values, 1000):
            # @todo move to db related files
            query = """
            SELECT upper(hash), song_fk, offset
            FROM fingerprints
            WHERE upper(hash) IN (%s)
            """
            query = query % ', '.join('?' * len(split_values))
        x = self.executeAll(query, split_values)
        matches_found = len(x)

        # if matches_found > 0:
        #     msg = '   ** found %d hash matches (step %d/%d)'
        #     print(colored(msg, 'green') % (matches_found,-1,len(values) ))
        # else:
        #     msg = '   ** not matches found (step %d/%d)'
        #     print(colored(msg, 'red') % (len(split_values),len(values) ))
        for hash, sid, offset in x:
            # (sid, db_offset - song_sampled_offset)
            yield (sid, offset - mapper[hash])
