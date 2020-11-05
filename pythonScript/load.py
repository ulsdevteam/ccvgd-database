from methods_for_sql import delete_data_from_table, insert_into_table
from read_file import read_csv_file, write_csv_file


def load_data_into_table(file_name, table_name, insert_sql, cnx, read_path = "Database data", write_path = "incorrect_records"):
    """
    insert data from file into table.

    :param file_name: csv file to be load into database
    :param table_name: table that stores the data from csv file
    :param insert_sql: sql to insert data
    :param cnx: MySQL connector object
    :param read_path: path to csv file
    :param write_path: path to incorrect records
    """

    # read file:
    data, csv_header = read_csv_file(read_path + "/" + file_name)

    # Delete data in table (necessary if reload)
    delete_data_from_table(table_name,cnx)

    # insert data into table, data should be able to be directly inserted into table
    incorrect_records = insert_into_table(insert_sql, data, cnx)

    # write incorrect records
    if len(incorrect_records) > 0:
        write_csv_file(write_path, table_name, csv_header, incorrect_records)
    else:
        print("All rows in {} are inserted into table {} successfully.".format(file_name, table_name))