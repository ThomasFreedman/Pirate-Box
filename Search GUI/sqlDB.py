#!/usr/bin/python3
from datetime import *
import sqlite3
import ipfs
import os

# Class for SQLite related code

class sql:
    def __init__(self):
        self.Conn = None
        self.Ipfs = ipfs.Ipfs()

    # Open the SQLite database obtained from IPNS
    def openDatabase(self, server):
        if self.Conn: self.Conn.close()     # Close database if previous opened
        self.Conn = sqlite3.connect(self.Ipfs.getDB(server))
        self.Conn.row_factory = sqlite3.Row # Results as a python dictionary

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
        return sql.runQuery(self, query)[0][0]




