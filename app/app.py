#!/usr/bin/env python3

import apistar
import logging
import os
import sqlite3
import sys
import urllib.request

"""
This is a dynamic DNS updater.
It is designed to run as a linux container on the system to be monitored.
Using apistar and a simple sqlite3 database, the program will
check the ip address it is connected to and update the database as necessary.
It will then connect to Route53 and update the DNS record as necessary.
Might have it do other stuff too as I think about it...
"""

logging.basicConfig(stream=sys.stderr, level=logging.CRITICAL)
dir_path = os.path.dirname(os.path.realpath(__file__))
sites_path = r"../sitestocheck/"
db_path = r"../db/"
db_file = "addresschanges.db"

# From https://www.sqlitetutorial.net/sqlite-python/create-tables/


def create_connection(db_file):
    """ create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
        """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def create_db():
    database = os.path.join(db_path, db_file)

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS ipchanges (
                                    id integer PRIMARY KEY,
                                    ip_address text NOT NULL,
                                    change_date text,
                                    site_checked text
                                    ); """

# create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create ipchanges table
        create_table(conn, sql_create_projects_table)

    else:
        print("Error! cannot create the database connection.")


def main():
    create_db


if __name__ == '__main__':
    main()
