from methods_for_sql import delete_data_from_table, insert_into_table
from read_file import read_csv_file, write_csv_file


def load_data_into_table(file_name, table_name, insert_sql, cnx, read_path="Database data",
                         write_path="incorrect_records"):
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
    delete_data_from_table(table_name, cnx)

    # insert data into table, data should be able to be directly inserted into table
    incorrect_records = insert_into_table(insert_sql, data, cnx)

    # write incorrect records
    if len(incorrect_records) > 0:
        write_csv_file(write_path, table_name, csv_header, incorrect_records)
    else:
        print("All rows in {} are inserted into table {} successfully.".format(file_name, table_name))


files_name = ("gazetteerInformation_村志信息.csv",
              "village_村.csv",
              "province_省.csv",
              "city_市.csv",
              "county_县.csv",
              "villageCountyCityProvince_村县市省.csv",
              "economyCategory_经济类.csv",
              "educationCategory_教育类.csv",
              "ethnicGroupsCategory_民族类.csv",
              "naturalDisastersCategory_自然灾害类.csv")

tables_name = ("gazetteerInformation_村志信息",
               "village_村",
               "province_省",
               "city_市",
               "county_县",
               "villageCountyCityProvince_村县市省",
               "economyCategory_经济类",
               "educationCategory_教育类",
               "ethnicGroupsCategory_民族类",
               "naturalDisastersCategory_自然灾害类")

sqls = ("INSERT INTO gazetteerInformation_村志信息 "
        "(gazetteerId_村志代码, gazetteerTitle_村志书名, gazetteerTitleHanyuPinyin_村志书名汉语拼音, yearOfPublication_出版年, publicationType_出版类型) "
        "VALUES (%s, %s, %s, %s, %s)",

        "INSERT INTO `village_村` "
        "(`villageInnerId_村庄内部代码`, `gazetteerId_村志代码`, `villageId_村庄代码`, `nameChineseCharacters_村名汉字`, `nameHanyuPinyin_村名汉语拼音`) "
        "VALUES (%s, %s, %s, %s, %s);",

        "INSERT INTO province_省 "
        "(provinceId_省代码, nameChineseCharacters_省汉字, nameHanyuPinyin_省汉语拼音) VALUES (%s, %s, %s)",

        "INSERT INTO city_市 "
        "(cityId_市代码, nameChineseCharacters_市汉字, nameHanyuPinyin_市汉语拼音) VALUES (%s, %s, %s)",

        "INSERT INTO county_县 "
        "(countyDistrictId_县或区代码, nameChineseCharacters_县或区汉字, nameHanyuPinyin_县或区汉语拼音) "
        "VALUES (%s, %s, %s)",

        "INSERT INTO villageCountyCityProvince_村县市省 "
        "(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `countyDistrictId_县或区代码`, `cityId_市代码`, `provinceId_省代码`) "
        "VALUES (%s, %s, %s, %s, %s)",

        "INSERT INTO `economyCategory_经济类`(`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `educationCategory_教育类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `ethnicGroupsCategory_民族类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `naturalDisastersCategory_自然灾害类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);")
