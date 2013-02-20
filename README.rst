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
