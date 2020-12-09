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
              "economyUnit_经济单位.csv",
              "economy_经济.csv",
              "educationCategory_教育类.csv",
              "educationUnit_教育单位.csv",
              "education_教育.csv",
              "ethnicGroupsCategory_民族类.csv",
              "ethnicGroupsUnit_民族单位.csv",
              "ethnicGroups_民族.csv",
              "naturalDisastersCategory_自然灾害类.csv",
              "naturalDisasters_自然灾害.csv",
              "lastNameCategory_姓氏类别.csv",
              "lastName_姓氏.csv",

              "populationcategory_人口类.csv",
              "populationUnit_人口单位.csv",
              "population_人口.csv",

              "militarycategory_军事类.csv",
              "militaryUnit_军事单位.csv",
              "military_军事.csv",

              "famliyplanningcategory_计划生育类.csv",
              "familyplanningUnit_计划生育单位.csv",
              "familyplanning_计划生育.csv",

              "naturalenvironmentcategory_自然环境类.csv",
              "naturalenvironmentUnit_自然环境单位.csv",
              "naturalenvironment_自然环境.csv",

              "villagegeographycategory_村庄地理类.csv",
              "villagegeographyUnit_村庄地理单位.csv",
              "villagegeography_村庄地理.csv"
              )

tables_name = ("gazetteerInformation_村志信息",
               "village_村",
               "province_省",
               "city_市",
               "county_县",
               "villageCountyCityProvince_村县市省",
               "economyCategory_经济类",
               "economyUnit_经济单位",
               "economy_经济",
               "educationCategory_教育类",
               "educationUnit_教育单位",
               "education_教育",
               "ethnicGroupsCategory_民族类",
               "ethnicGroupsUnit_民族单位",
               "ethnicGroups_民族",
               "naturalDisastersCategory_自然灾害类",
               "naturalDisasters_自然灾害",

               "lastNameCategory_姓氏类别",
               "lastName_姓氏",

               "populationcategory_人口类",
               "populationUnit_人口单位",
               "population_人口",

               "militarycategory_军事类",
               "militaryUnit_军事单位",
               "military_军事",

               "familyplanningcategory_计划生育类",
               "familyplanningUnit_计划生育单位",
               "familyplanning_计划生育",

               "naturalenvironmentcategory_自然环境类",
               "naturalenvironmentUnit_自然环境单位",
               "naturalenvironment_自然环境",

               "villagegeographycategory_村庄地理类",
               "villagegeographyUnit_村庄地理单位",
               "villagegeography_村庄地理"
               )

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

        "INSERT INTO `economyUnit_经济单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `economy_经济` "
        "(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`, `startYear_开始年`, `endYear_结束年`, `unitId_单位代码`, `data_数据`) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `educationCategory_教育类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `educationUnit_教育单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `education_教育` "
        "(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`, `startYear_开始年`, `endYear_结束年`, `unitId_单位代码`, `data_数据`) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `ethnicGroupsCategory_民族类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `ethnicGroupsUnit_民族单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `ethnicGroups_民族` "
        "(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`, `startYear_开始年`, `endYear_结束年`, `unitId_单位代码`, `data_数据`) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `naturalDisastersCategory_自然灾害类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `naturalDisasters_自然灾害` (`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`, `year_年份`) VALUES (%s, %s, %s, %s);",

        "INSERT INTO `lastNameCategory_姓氏类别` (`categoryId_类别代码`, `nameChineseCharacters_姓氏汉字`, `nameHanyuPinyin_姓氏汉语拼音`) VALUES (%s, %s, %s);",

        "INSERT INTO `lastName_姓氏` "
        "(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `firstlastNamesId_姓氏代码`, `secondlastNamesId_姓氏代码`, `thirdlastNamesId_姓氏代码`, `fourthlastNamesId_姓氏代码`, `fifthlastNamesId_姓氏代码`, `totalNumberofLastNamesinVillage_姓氏总数`) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `populationcategory_人口类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `populationUnit_人口单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `population_人口`(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`,`startYear_开始年`, `endYear_结束年`, `unitId_单位代码`, `data_数据`) VALUES (%s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `militarycategory_军事类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `militaryUnit_军事单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `military_军事`(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`,`startYear_开始年`, `endYear_结束年`, `unitId_单位代码`, `data_数据`) VALUES (%s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `familyplanningcategory_计划生育类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `familyplanningUnit_计划生育单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `familyplanning_计划生育`(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`,`startYear_开始年`, `endYear_结束年`, `unitId_单位代码`, `data_数据`) VALUES (%s, %s, %s, %s, %s, %s, %s);",

        "INSERT INTO `naturalenvironmentcategory_自然环境类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `naturalenvironmentUnit_自然环境单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `naturalenvironment_自然环境`(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`, `unitId_单位代码`, `data_数据`) VALUES (%s, %s, %s, %s, %s);",

        "INSERT INTO `villagegeographycategory_村庄地理类` (`categoryId_类别代码`, `name_名称`, `parentId_父类代码`) VALUES (%s, %s, %s);",

        "INSERT INTO `villagegeographyUnit_村庄地理单位` (`unitId_单位代码`, `name_名称`) VALUES (%s, %s);",

        "INSERT INTO `villagegeography_村庄地理`(`gazetteerId_村志代码`, `villageInnerId_村庄内部代码`, `categoryId_类别代码`, `unitId_单位代码`, `data_数据`) VALUES (%s, %s, %s, %s, %s);"
        )
