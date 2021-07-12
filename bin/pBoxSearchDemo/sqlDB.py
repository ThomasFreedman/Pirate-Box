#!/usr/bin/python3
import sqlite3

# Class for SQLite related code

class sql:
    def __init__(self, ipfs):
        self.Server = None
        self.Conn = None
        self.Ipfs = ipfs

    # Open the SQLite database, which may come from IPFS or local storage.
    # Databases coming from IPFS are cached locally. See ipfs module for details.
    def openDatabase(self, server, gui, x, y):
        try:
            if self.Conn:
                self.Conn.close()     # Close database if previous opened
                self.Conn = None
            self.Conn = sqlite3.connect(self.Ipfs.getDB(server, gui, x, y))
            self.Conn.row_factory = sqlite3.Row # Results as a python dictionary
            self.Sever = server
        except Exception as e:
            pass

    # Execute a SQL query and return the result set as an array of dictionaries
    # rs[0] = { column name 1: value, column 2: value, column 3: value ...}
    def runQuery(self, query):
        try:
            rs = []
            rs = self.Conn.cursor().execute(query).fetchall()
        except sqlite3.OperationalError as e:
            pass  # ignore for now
        return rs

    # Perform a SQL query that selects only 1 column and return the results in a list
    # This is used to populate listboxes, checkboxes, radio buttons etc.
    def getListFromSql(self, query):
        out = []
        for r in sql.runQuery(self, query):
            out.append(r[0])
        return out
 
    def getHash(self, key):
        query = f"SELECT vhash from IPFS_HASH_INDEX WHERE pky={key}"
        try:
            sql.runQuery(self, query)[0][0]
            return sql.runQuery(self, query)[0][0]
        except:
            return ""


