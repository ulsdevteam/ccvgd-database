import mysql.connector
from mysql.connector import errorcode

def connect_to_mysql(config):
    """
    connect to mysql server

    :param config: dictionary contains configure parameters.
    :return: cnx,MySQL connection object.
    """

    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)
            exit(1)
    else:
        print("successfully connect to mysql")
        return cnx

def switch_to_database(cnx, DB_NAME):
    """
    switch to the database schema whose name is DB_NAME,
    if schema does not exists, try to create the schema.

    :param cnx: MySQL connection object
    :param DB_NAME: name of database schema
    """

    try:
        cursor = cnx.cursor()
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cnx, DB_NAME)
            print("Database {} created successfully.".format(DB_NAME))
            cnx.database = DB_NAME
            cursor.close()
        else:
            print(err)
            cursor.close()
            exit(1)
    else:
        print("Switch to schema {}".format(DB_NAME))
        cnx.database = DB_NAME
        cursor.close()

def create_database(cnx, DB_NAME):
    """
    create the schema using name DB_NAME

    :param cnx: MySQL connection object
    :param DB_NAME: name of database to be created
    :return: cnx, the MySQL connection object
    """
    cursor = cnx.cursor()
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        cursor.close()
        exit(1)
    else:
        print("Create schema {} success".format(DB_NAME))
        cnx.commit()
        cnx.database = DB_NAME
        cursor.close()

def create_tables(TABLES, cnx):

    """
    create 36 predefined tables

    :param TABLES: dictionary contains predefined CREAT SQL statement
    :param cursor: an object of MySQLCursor class
    """

    for table_name in TABLES:
        cursor = cnx.cursor()
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")
        cursor.close()