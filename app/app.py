#!/usr/bin/env python3

import apistar
import datetime
import ipaddress
import logging
import os
import socket
import sqlite3
import urllib.request

"""
This is a dynamic DNS updater.
It is designed to run as a linux container on the system to be monitored.
Using apistar and a simple sqlite3 database, the program will
check the ip address it is connected to and update the database as necessary.
It will then connect to Route53 and update the DNS record as necessary.
Might have it do other stuff too as I think about it...
"""

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


dir_path = os.path.dirname(os.path.realpath(__file__))
sites_path = r"../sitestocheck/"
db_path = r"../db/"
db_file = "addresschanges.db"
database = os.path.join(dir_path, db_path, db_file)


# From https://www.sqlitetutorial.net/sqlite-python/create-tables/


def create_connection(db_file):
    """create a database connection to the SQLite database
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
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def create_db(database):

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


def create_entry(conn, entry):
    """
    Create a new entry into the ipchanges table
    :param conn:
    :param entry:
    :return: ipchanges id
    """
    sql = ''' INSERT INTO ipchanges(ip_address,change_date,site_checked)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, entry)
    conn.commit()
    return cur.lastrowid


def is_connected():
    try:
        # connect to the host -- tells us if the internet connection is live
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def get_ip(site):
    try:
        req = urllib.request.Request(site)
        response = urllib.request.urlopen(req)
        target_ip = response.read().decode("utf-8")
        try:
            ipaddress.IPv4Address(target_ip)
            return target_ip
        except ipaddress.AddressValueError as e:
            return f"address_error {e}"

    except urllib.error.URLError as e:
        return f"URLError {e}"


def main():
    create_db(database)

    if is_connected():
        found_ip = get_ip("https://api.ipify.org/")
        conn = create_connection(database)

    with conn:
        timestamp = datetime.datetime.now()
        entry = (found_ip, timestamp, "ipify.org")
        create_entry(conn, entry)
        logger.INFO(f"entry is {entry}")


if __name__ == "__main__":
    main()
