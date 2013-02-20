#!/usr/bin/python
# -*- coding: utf-8 -*-
from .util import import_module


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
        def _route_db(self, model, **hints):
            chosen_db = None
            for router in self.routers:
                try:
                    method = getattr(router, action)
                except AttributeError:
                    # If the router doesn't have a method, skip to the next one.
                    pass
                else:
                    chosen_db = method(model, **hints)
                    if chosen_db:
                        return chosen_db
            return DEFAULT_DB_ALIAS
        return _route_db

    db_for_read = _router_func('db_for_read')
    db_for_write = _router_func('db_for_write')
