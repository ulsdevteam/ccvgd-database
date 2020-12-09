import pandas as pd

def validate_pinyin(group_by_result):
    """
    find provinces/cities/counties that have different pinyin recorded.

    On general, one province should only has one pinyin recorded.
    If one province/city/county has different pinyins recorded,
    manager should choose one correct pinyin and update other mistake pinyins.

    return: a list of (name, pinyin) tuples.
            dic2: contains provinces/cities/counties whoes pinyin was recorded incorrect.
    """

    dict1 = {}
    list_of_tuples = []

    # create name: [pinyin] mapping
    for name_pinyin, frame in group_by_result:
        name = name_pinyin[0]
        pinyin = name_pinyin[1]
        if name not in dict1:
            dict1[name] = []
            dict1[name].append(pinyin)
            list_of_tuples.append((name, pinyin))
        else:
            dict1[name].append(pinyin)

        # a bug in csv file fixed by this
        dict1["旅顺口区"] = ["Lüshunkou Qu"]

    # find provinces/cities/counties that have different pinyin recorded
    dict2 = {}
    for key in dict1:
        if (len(dict1[key])) > 1:
            dict2[key] = dict1[key]

    return list_of_tuples, dict2

def print_incorrect_pinyin(name, mistake):
    """
    print province/city/county which was recorded with more than one pinyin.

    :param filename: province/county/city
    :param mistake: dictionary store {"name":[pinyin1, pinyin2,...]}
    """
    print("{} with multiple pinyin recorded:".format(name))
    [print(key, value) for key, value in mistake.items()]
    print("------------------------")


def create_csv_city_county_province(read_path, output_path, read_file_name):
    """
    create province_省.csv, city_市.csv, county_县.csv for province_省, city_市, county_县 tables.

    :param read_path: path for "Village Information.csv".
    :param read_file_name: "Village Information.csv".
    :param output_path: path to directory where stores province_省.csv, city_市.csv, county_县.csv.
    """
    # Read village.csv file
    villages = pd.read_csv(read_path + "/" + read_file_name)

    print("Creat province_省.csv, city_市.csv, county_县.csv")
    # create data for database
    group_by_province = villages.groupby(["省 - 汉字 Province - Chinese Characters", "省 - 汉语拼音 Province - Hanyu Pinyin"])
    province_in_csv, province_mistake = validate_pinyin(group_by_province)

    group_by_city = villages.groupby(["市 - 汉字 City - Chinese Characters", "市 - 汉语拼音 City - Hanyu Pinyin"])
    city_in_csv, city_mistake = validate_pinyin(group_by_city)

    group_by_county = villages.groupby(
        ["县 / 区 - 汉字 County / District - Chinese Characters", "县 / 区 - 汉语拼音 County / District - Hanyu Pinyin"])
    county_in_csv, county_mistake = validate_pinyin(group_by_county)

    # check for incorrect records
    if province_mistake != {} or city_mistake != {} or county_mistake != {}:
        print_incorrect_pinyin("provinces", province_mistake)
        print_incorrect_pinyin("cities", city_mistake)
        print_incorrect_pinyin("counties", county_mistake)
        exit(1)

    # output
    province_df = pd.DataFrame(province_in_csv, columns=["name", "pinyin"])
    province_df.insert(0, 'id', province_df.index + 1)  # create province id
    province_df.to_csv(output_path + "/" + "province_省.csv", index=False, na_rep="NULL")

    city_df = pd.DataFrame(city_in_csv, columns=["name", "pinyin"])
    city_df.insert(0, 'id', city_df.index + 1)  # create city id
    city_df.to_csv(output_path + "/" + "city_市.csv", index=False, na_rep="NULL")

    county_df = pd.DataFrame(county_in_csv, columns=["name", "pinyin"])
    county_df.insert(0, 'id', county_df.index + 1)  # create county id
    county_df.to_csv(output_path + "/" + "county_县.csv", index=False, na_rep="NULL")

    print("Finish province_省.csv, city_市.csv, county_县.csv")


def create_csv_village_and_address(read_path, output_path, read_file_name):
    """
    create village_村.csv for village_村 table, villageCountyCityProvince_村县市省.csv for villageCountyCityProvince_村县市省 table.

    :param read_path: path for "Village Information.csv".
    :param read_file_name: "Village Information.csv".
    :param output_path: path to directory where stores village_村.csv, villageCountyCityProvince_村县市省.csv.
    """
    # ---- Read Village Information.csv file ----
    villages_df = pd.read_csv(read_path + "/" + read_file_name, dtype={"村庄代码 Village Code": str})

    # ---- Create Village Inner ID ------
    # ---- village inner id equals to gazetteer id
    villages_df["village_inner_id"] = villages_df["村志代码 Gazetteer Code"]

    # ---- Create village_村.csv ------
    print("Create village_村.csv")
    village = pd.DataFrame({'villageInnerId_村庄内部代码': villages_df["village_inner_id"].values,
                            'gazetteerId_村志代码': villages_df["村志代码 Gazetteer Code"].values,
                            'villageId_村庄代码': villages_df["村庄代码 Village Code"].values,
                            'nameChineseCharacters_村名汉字': villages_df[
                                '村名 - 汉字 Village Name - Chinese Characters'].values,
                            'nameHanyuPinyin_村名汉语拼音': villages_df['村名 - 汉语拼音 Village Name - Hanyu Pinyin'].values})
    print("Finish village_村.csv.")

    # ---- Create villageCountyCityProvince_村县市省.csv ------
    print("Create villageCountyCityProvince_村县市省.csv")
    # read previous created province, city, county id mapping
    province_df = pd.read_csv(output_path + "/" + "province_省.csv", dtype={'id': int})
    province_df.columns = ["province_id", "province_name", "province_pinyin"]
    county_df = pd.read_csv(output_path + "/" + "county_县.csv", dtype={'id': int})
    county_df.columns = ["county_id", "county_name", "county_pinyin"]
    city_df = pd.read_csv(output_path + "/" + "city_市.csv", dtype={'id': int})
    city_df.columns = ["city_id", "city_name", "city_pinyin"]

    # left join
    village_address = pd.merge(villages_df, province_df, left_on='省 - 汉字 Province - Chinese Characters',
                               right_on='province_name', how='left')
    village_address = pd.merge(village_address, city_df, left_on='市 - 汉字 City - Chinese Characters',
                               right_on='city_name', how='left')
    village_address = pd.merge(village_address, county_df, left_on='县 / 区 - 汉字 County / District - Chinese Characters',
                               right_on='county_name', how='left')
    # data for villageCountyCityProvince_村省市县 table
    village_address = pd.DataFrame({'gazetteerId_村志代码': village_address['村志代码 Gazetteer Code'].values,
                                    'villageInnerId_村庄内部代码': village_address["village_inner_id"].values,
                                    'countyId_县区代码': village_address["county_id"],
                                    'cityId_市代码': village_address["city_id"],
                                    'provinceId_省代码': village_address["province_id"]})
    print("Finish villageCountyCityProvince_村县市省.csv.")

    # ---- write data ----
    village.to_csv(output_path + "/" + "village_村.csv", index=False, na_rep="NULL")
    village_address.to_csv(output_path + "/" + "villageCountyCityProvince_村县市省.csv", index=False, na_rep="NULL")
