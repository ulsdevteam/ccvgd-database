from load import load_data_into_table, files_name, tables_name, sqls
from connect import connect_to_mysql, switch_to_database, read_config_parameter
from methods_for_sql import create_tables
from Table import Table

# read config parameter
config, DB_NAME = read_config_parameter("config.txt")
# connect to mysql
cnx = connect_to_mysql(config)

# drop the DB_NAME database, if previous exists
cursor = cnx.cursor()
cursor.execute("DROP DATABASE IF EXISTS {};".format(DB_NAME))
cursor.close()

# switch to database
switch_to_database(cnx, DB_NAME)

# create 36 tables under the database
TABLES = Table.TABLES # TABLES: predefined CREATE SQL commands
create_tables(TABLES, cnx)

read_path = "Database data"
write_path = "incorrect_records"
for file, table_name, sql in zip(files_name, tables_name, sqls):
    load_data_into_table(file,table_name,sql,cnx,read_path,write_path)

cnx.close()
