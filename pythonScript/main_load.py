from load import load_data_into_table
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

# gazetteerInformation_村志信息.csv
file_name = "gazetteerInformation_村志信息.csv"
table_name = "gazetteerInformation_村志信息"
sql = ("INSERT INTO gazetteerInformation_村志信息 "
               "(gazetteerId_村志代码, gazetteerTitle_村志书名, gazetteerTitleHanyuPinyin_村志书名汉语拼音, yearOfPublication_出版年, publicationType_出版类型) "
               "VALUES (%s, %s, %s, %s, %s)")
load_data_into_table(file_name, table_name, sql, cnx, read_path,write_path)

# village_村.csv
file_name = "village_村.csv"
table_name = "village_村"
sql = ("INSERT INTO `village_村` "
       "(`villageInnerId_村庄内部代码`, `gazetteerId_村志代码`, `villageId_村庄代码`, `nameChineseCharacters_村名汉字`, `nameHanyuPinyin_村名汉语拼音`) "
       "VALUES (%s, %s, %s, %s, %s);")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)

# province_省.csv
file_name = "province_省.csv"
table_name = "province_省"
sql = ("INSERT INTO province_省 "
               "(provinceId_省代码, nameChineseCharacters_省汉字, nameHanyuPinyin_省汉语拼音) "
               "VALUES (%s, %s, %s)")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)

# city_市.csv
file_name = "city_市.csv"
table_name = "city_市"
sql = ("INSERT INTO city_市 "
               "(cityId_市代码, nameChineseCharacters_市汉字, nameHanyuPinyin_市汉语拼音) "
               "VALUES (%s, %s, %s)")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)

# county_县.csv
file_name = "county_县.csv"
table_name = "county_县"
sql = ("INSERT INTO county_县 "
               "(countyDistrictId_县或区代码, nameChineseCharacters_县或区汉字, nameHanyuPinyin_县或区汉语拼音) "
               "VALUES (%s, %s, %s)")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)

# villageCountyCityProvince_村县市省.csv
file_name = "villageCountyCityProvince_村县市省.csv"
table_name = "villageCountyCityProvince_村县市省"
sql = ("INSERT INTO villageCountyCityProvince_村县市省 "
               "(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `countyDistrictId_县或区代码`, `cityId_市代码`, `provinceId_省代码`) "
               "VALUES (%s, %s, %s, %s, %s)")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)

# economyCategory_经济类.csv
file_name = "economyCategory_经济类.csv"
table_name = "economyCategory_经济类"
sql = ("INSERT INTO `economyCategory_经济类` "
       "(`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) "
       "VALUES (%s, %s, %s);")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)

# economyUnit_经济单位.csv
file_name = "economyUnit_经济单位.csv"
table_name = "economyUnit_经济单位"
sql = ("INSERT INTO `economyUnit_经济单位` "
       "(`unitId_单位代码`, `name_名称`) "
       "VALUES (%s, %s);")
load_data_into_table(file_name,table_name,sql,cnx,read_path,write_path)



cnx.close()