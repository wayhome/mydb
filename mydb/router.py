#!/usr/bin/python
# -*- coding: utf-8 -*-
from .util import import_module
from .pinning import this_thread_is_pinned

DEFAULT_DB_ALIAS = 'default'


class ConnectionRouter(object):
    def __init__(self, routers):
        self.routers = []
        for r in routers:
            if isinstance(r, basestring):
                try:
                    module_name, klass_name = r.rsplit('.', 1)
                    module = import_module(module_name)
                except ImportError, e:
                    raise ImproperlyConfigured('Error importing database router %s: "%s"' % (klass_name, e))
                try:
                    router_class = getattr(module, klass_name)
                except AttributeError:
                    raise ImproperlyConfigured('Module "%s" does not define a database router name "%s"' % (module, klass_name))
                else:
                    router = router_class()
            else:
                router = r
            self.routers.append(router)

    def _router_func(action):
        def _route_db(self, statement, **hints):
            chosen_db = None
            for router in self.routers:
                try:
                    method = getattr(router, action)
                except AttributeError:
                    # If the router doesn't have a method, skip to the next one.
                    pass
                else:
                    chosen_db = method(statement, **hints)
                    if chosen_db:
                        return chosen_db
            return DEFAULT_DB_ALIAS
        return _route_db

    db_for_read = _router_func('db_for_read')
    db_for_write = _router_func('db_for_write')


class MasterSlaveRouter(object):
    """Router that sends all reads to a slave, all writes to default."""

    def db_for_read(self, statement, **hints):
        """Send reads to slaves in round-robin."""
        return self.get_slave()

    def db_for_write(self, statement, **hints):
        """Send all writes to the master."""
        return self.get_master()

    def get_slave(self):
        raise NotImplemented

    def get_master(self):
        raise NotImplemented


class PinningMasterSlaveRouter(MasterSlaveRouter):
    """Router that sends reads to master iff a certain flag is set. Writes
    always go to master.

    Typically, we set a cookie in middleware when the request is a POST and
    give it a max age that's certain to be longer than the replication lag. The
    flag comes from that cookie.

    """
    def db_for_read(self, statement, **hints):
        """Send reads to slaves in round-robin unless this thread is "stuck" to
        the master."""
        return self.get_master() if this_thread_is_pinned() else self.get_slave()
