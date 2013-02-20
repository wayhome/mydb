#!/usr/bin/python
# -*- coding: utf-8 -*-
import functools


class DBProxy(object):

    def __init__(self, router):
        self.router = router

    def __wrap(self, method, statement, *args, **kwargs):
        if statement.strip().upper().startswith("SELECT"):
            db = self.router.db_for_read(statement)
        else:
            db = self.router.db_for_write(statement)
        f = getattr(db, method)
        return f(statement, *args, **kwargs)

    def __getattr__(self, method):
        return functools.partial(self.__wrap, method)
