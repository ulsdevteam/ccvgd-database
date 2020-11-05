import pandas as pd

def iterate_group_by(group_by_result):
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

    :param filename: province/county/city
    :param mistake: dictionary store {"name":[pinyin1, pinyin2,...]}
    """
    print("{} with multiple pinyin recorded:".format(name))
    [print(key, value) for key, value in mistake.items()]
    print("------------------------")

def create_city_county_province_tables(read_path, read_file_name, output_path):

    # Read village.csv file
    villages = pd.read_csv(read_path + "/" + read_file_name)

    print("Creat province_省.csv, city_市.csv, county_县.csv")
    # create data for database
    group_by_province = villages.groupby(["省 - 汉字 Province - Chinese Characters", "省 - 汉语拼音 Province - Hanyu Pinyin"])
    province_in_csv, province_mistake = iterate_group_by(group_by_province)

    group_by_city = villages.groupby(["市 - 汉字 City - Chinese Characters", "市 - 汉语拼音 City - Hanyu Pinyin"])
    city_in_csv, city_mistake = iterate_group_by(group_by_city)

    group_by_county = villages.groupby(["县 / 区 - 汉字 County / District - Chinese Characters", "县 / 区 - 汉语拼音 County / District - Hanyu Pinyin"])
    county_in_csv, county_mistake = iterate_group_by(group_by_county)

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
