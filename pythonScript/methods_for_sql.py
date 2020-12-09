import mysql.connector
from mysql.connector import errorcode

def delete_data_from_table(table_name, cnx):
    """
    Perform DELETE FROM table_name query.
    Delete all data from the table.

    :param table_name: name of table
    :param cnx: Mysql connector object
    """

    cursor = cnx.cursor()
    delete_sql = "Delete from {}".format(table_name)
    try:
        cursor.execute(delete_sql)
    except mysql.connector.Error as error:
        print(error)
        cnx.rollback()
    else:
        print("------------")
        print("DELETE data of {}".format(table_name))
        cnx.commit()
    cursor.close()

def insert_into_table(insert_sql, data, cnx):
    """
    Perform predefined INSERT sql.

    :param insert_sql: sql to insert data
    :param data: a list of tuples contains data to be inserted
    :param cnx: MySQL connector
    :return: not correct records which should be fixed.
             incorrect_records: A list of tuples that each tuple is a incorrect record.
    """
    incorrect_records = []
    # insert records into table
    count = 0
    for one_record in data:
        cursor = cnx.cursor()
        try:
            cursor.execute(insert_sql, one_record)
        except mysql.connector.Error as error:
            # skip error for duplicate record
            if error.errno == 1062:
                cnx.rollback()
                continue
            # process other errors
            print(error)
            incorrect_records.append(one_record)
            cnx.rollback()
        else:
            cnx.commit()
        cursor.close()
        count += 1
        if count % 5000 == 0:
            print("finish {} records".format(count))

    print("Finished inserting data.")
    return incorrect_records


def select_all_from_table(table_name, cnx):
    """
    perform SELECT * FROM table_name query

    :param table_name: name of table
    :param cnx: MySQL connector object
    :return: a list of tuples contains all data
    """

    cursor = cnx.cursor()
    # format query
    query = ("SELECT * FROM {}".format(table_name))
    try:
        cursor.execute(query)
    except mysql.connector.Error as error:
        print(error)
        exit(1)
    else:
        print("Successfully SELECT * FROM {}.".format(table_name))

    data = cursor.fetchall()
    cursor.close()

    return data

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
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(error.msg)
        else:
            print("OK")
        cursor.close()