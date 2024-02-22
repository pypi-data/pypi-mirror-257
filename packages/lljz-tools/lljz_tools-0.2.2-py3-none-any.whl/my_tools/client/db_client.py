# coding=utf-8

"""
@fileName       :   db_client.py
@data           :   2024/2/8
@author         :   jiangmenggui@hosonsoft.com
"""
import re

import pymysql
from pymysql.cursors import DictCursor

from my_tools.attribute_dict import AttributeDict
from my_tools.decorators import debug




class DBConnection(AttributeDict, total=True, variable=False, check_type=True):
    host: str
    port: int
    db_name: str
    user: str = ''
    password: str = ''


class MySQLClient:

    def __init__(self, uri: str):
        obj = re.match(
            r'^mysql://(?P<user>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<db_name>.+)$',
            uri
        )
        if not obj:
            raise ValueError('uri is wrong!')
        self.connection = DBConnection(obj.groupdict())

    def connect(self):
        return _MySQLContext(**self.connection)


class _MySQLContext:

    def __init__(self, user, password, host, port, db_name):
        self.con = pymysql.connect(host=host, port=port, user=user, password=password, database=db_name)
        self.cur = self.con.cursor(DictCursor)
        self.cur.commit = self.con.commit
        self.cur.rollback = self.con.rollback

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()


if __name__ == '__main__':
    with MySQLClient('mysql://root:myroot123!@127.0.0.1:3306/server_monitor').connect() as client:
        client.execute('select * from information_schema.TABLES where TABLE_SCHEMA=%s', ['server_monitor'])
        print(client.fetchall())
