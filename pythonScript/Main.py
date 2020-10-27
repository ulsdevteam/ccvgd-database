import json

from Table import Table
from create_database import connect_to_mysql, switch_to_database, create_tables

# read cRonfig file
with open('config.txt') as f:
    file = json.load(f)

# config: dictionary stores parameters to connect to mySQL server
config = {}
config['user'] = file['user']
config['password'] = file['password']
config['host'] = file['host']

# DB_NAME: name of new database schema
DB_NAME = file['database']

# connect to mysql
# cnx: MySQL connection object
cnx = connect_to_mysql(config)

# drop the DB_NAME database, if previous exists
cursor = cnx.cursor()
cursor.execute("DROP DATABASE IF EXISTS {};".format(DB_NAME))
cursor.close()

# switch or create database schema
switch_to_database(cnx, DB_NAME)

# create 36 tables under the database
# TABLES: predefined CREATE SQL commands
TABLES = Table.TABLES
create_tables(TABLES, cnx)
cnx.close()


