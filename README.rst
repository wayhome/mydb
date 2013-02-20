mydb
================
db wrapper for mysql

Usage
================

Single Connection
--------------------


        from mydb.connection import Connection

        db = Connection("mysql://youngking@localhost:13306/mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title


Multiple Connection Like Master/Slave
-----------------------------------------

        from mydb.router import ConnectionRouter
        from mydb.proxy import DBProxy
        router = ConnectionRouter(["myapp.somewhere.MasterSlaveRouter"])
        proxy = DBProxy(router)

        for article in proxy.query("SELECT * FROM articles"):
            print article.title

Database routers
~~~~~~~~~~~~~~~~~~~

A database Router is a class that provides up to two methods:

db_for_read(statement, **hints)

    Suggest the database that should be used for read operations for ``SELECT`` statement.

    If a database operation is able to provide any additional information that might assist in selecting a database, it will be provided in the hints dictionary. Details on valid hints are provided below.

    Returns None if there is no suggestion.

db_for_write(model, **hints)

    Suggest the database that should be used for writes of statements except ``SELECT``.

    If a database operation is able to provide any additional information that might assist in selecting a database, it will be provided in the hints dictionary. Details on valid hints are provided below.


There is an example in ``tests/test_router.py``.
