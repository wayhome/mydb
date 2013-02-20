#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import unittest
import itertools


class TestRouter(unittest.TestCase):

    def setUp(self):
        from mydb.connection import Connection
        mysql_url = 'mysql://root@127.0.0.1:13306/'
        conn1 = Connection(os.path.join(mysql_url, 'zhweb_development'))
        conn2 = Connection(os.path.join(mysql_url, 'zhweb_test'))
        slaves = itertools.cycle([conn1, conn2])

        def get_slave():
            return slaves.next()

        class MasterSlaveRouter(object):
            """Router that sends all reads to a slave, all writes to default."""

            def db_for_read(self, model, **hints):
                """Send reads to slaves in round-robin."""
                return get_slave()

            def db_for_write(self, model, **hints):
                """Send all writes to the master."""
                return conn1

        from mydb.router import ConnectionRouter
        from mydb.proxy import DBProxy
        self.router = ConnectionRouter([MasterSlaveRouter()])
        #self.router = ConnectionRouter(["MasterSlaveRouter"])
        self.proxy = DBProxy(self.router)

    def test_router(self):
        print self.router.db_for_read("SELECT now();")
        print self.proxy.query("SELECT now();")
