import pandas as pd
from connect import connect_to_mysql, switch_to_database, read_config_parameter
from methods_for_sql import select_all_from_table

def create_village_and_address_tables(read_path, read_file_name, output_path):

    # ---- Read Village Information.csv file ----
    villages_df = pd.read_csv( read_path + "/" + read_file_name, dtype={"村庄代码 Village Code": str})

    # ---- Create Village Inner ID ------
    # ---- village inner id equals to gazetteer id
    villages_df["village_inner_id"] = villages_df["村志代码 Gazetteer Code"]

    # ---- Create village_村.csv ------
    print("Create village_村.csv")
    village = pd.DataFrame({'villageInnerId_村庄内部代码': villages_df["village_inner_id"].values,
                            'gazetteerId_村志代码': villages_df["村志代码 Gazetteer Code"].values,
                            'villageId_村庄代码': villages_df["村庄代码 Village Code"].values,
                            'nameChineseCharacters_村名汉字': villages_df['村名 - 汉字 Village Name - Chinese Characters'].values,
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
    village_address = pd.merge(villages_df, province_df, left_on='省 - 汉字 Province - Chinese Characters', right_on='province_name', how='left')
    village_address = pd.merge(village_address, city_df, left_on='市 - 汉字 City - Chinese Characters', right_on='city_name', how='left')
    village_address = pd.merge(village_address, county_df, left_on='县 / 区 - 汉字 County / District - Chinese Characters', right_on='county_name', how='left')
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


