#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest


class TestConn(unittest.TestCase):

    def setUp(self):
        from mydb.connection import Connection
        mysql_url = 'mysql://root@127.0.0.1:13306/'
        self.conn1 = Connection(os.path.join(mysql_url, 'zhweb_development'))
        self.conn2 = Connection(os.path.join(mysql_url, 'zhweb_test'))

    def test_conn1(self):
        assert self.conn1.query('SELECT now();') is not None

    def test_conn2(self):
        assert self.conn2.query('SELECT now();') is not None
