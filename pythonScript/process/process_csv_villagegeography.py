import pandas as pd
import math
import sys
import numpy as np
from process.validate_csv_data import mapping_id

def create_csv_villagegeography_Unit(read_path, output_path, input_file):
    """
    create villagegeography_村庄地理.csv, villagegeographyUnit_村庄地理单位.csv that will be loaded into database.

    Process data in "Village Information.csv" file to "villagegeography_村庄地理.csv", "villagegeographyUnit_村庄地理单位.csv" 
    Categories for naturalenvironment table is read from "Database Data" directory
    Categories are predefined and created.
    If categories are changed, naturalenvironment categories in Category.py should be changed first.

    :param read_path: path to directory contains "Village Information.csv"
    :param output_path: path to directory stores "villagegeography_村庄地理.csv", "villagegeographyUnit_村庄地理单位.csv" 
    :param input_file: file contains naturalenvironment data
    """
    df = pd.read_csv(read_path + "/" + input_file)

    df = df.dropna(axis=0, how='all')

    df.drop_duplicates(inplace=True)

    #---------------csv transpose -------------#
    # subset different column and then combine 3 dataframes together
    df1 = df[['村志代码 Gazetteer Code','村庄总面积 Total Area','村庄总面积单位 Total Area Unit']].copy()
    df1.loc[:,"category"] = '村庄总面积 Total Area'
    df1 = df1.rename(columns = {'村庄总面积 Total Area': 'data','村庄总面积单位 Total Area Unit':'Unit'})

    df2 = df[['村志代码 Gazetteer Code','纬度 Latitude','经纬度 - 格式 Latitude and Longitude - Format']].copy()
    df2.loc[:,"category"] = '纬度 Latitude'
    df2 = df2.rename(columns = {'纬度 Latitude': 'data','经纬度 - 格式 Latitude and Longitude - Format':'Unit'})

    df3 = df[['村志代码 Gazetteer Code','经度 Longitude','经纬度 - 格式 Latitude and Longitude - Format']].copy()
    df3.loc[:,"category"] = '经度 Longitude'
    df3 = df3.rename(columns = {'经度 Longitude': 'data','经纬度 - 格式 Latitude and Longitude - Format':'Unit'})

    df4 = df[['村志代码 Gazetteer Code','距隶属县城距离 Distance to Affiliated to the county town','距隶属县城距离单位 Distance to Affiliated to the county town - Unit']].copy()
    df4.loc[:,"category"] = '距隶属县城距离 Distance to Affiliated to the county town'
    df4 = df4.rename(columns = {'距隶属县城距离 Distance to Affiliated to the county town': 'data','距隶属县城距离单位 Distance to Affiliated to the county town - Unit': 'Unit'})
    # combine 4 subset dataframe to df5
    df5 = df1.append([df2,df3,df4]) # df5 = [村志代码 Gazetteer Code, data, unit, category]

    # create "level1" column using "category" column
    df5['level1'] = df5['category'] # df5 = [村志代码 Gazetteer Code, data, unit, category, level1]

    #df5.to_csv(output_path + "test.csv",encoding='utf-8-sig')
    #print("df5 to csv done")

    #---------------csv using "villagegrography_村庄地理类.csv" to code "category_id" column -------------#
    # group by categories
    groupby_categories = df5.groupby(['level1'])
    
    geography_df = pd.DataFrame()
    category_df = pd.read_csv("Database data/villagegeographycategory_村庄地理类.csv")

    # add "category_id"
    for group, frame in groupby_categories:
      
        level1_category = group

        parent_id = math.nan
        if level1_category != "":
            category_id = mapping_id(level1_category, parent_id, category_df)
            #parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        geography_df = pd.concat([geography_df, frame])
    
    #---------------create "villagegrographyUnit.csv" -------------#
    # create unit - id mapping
    units = geography_df['Unit'].unique().tolist()
    # df for naturalenvironmentUnit.csv
    geoUnit = pd.DataFrame({'unit_id': list(range(1, len(units) + 1)), 'name': units})


    # append unit id
    geography_df = pd.merge(geography_df, geoUnit, left_on='Unit', right_on='name', how='left')

    # df for naturalenvironment_自然环境.csv
    naturalenv = pd.DataFrame({'gazetteerId': geography_df['村志代码 Gazetteer Code'],
                            'villageInnerId': geography_df['村志代码 Gazetteer Code'],
                            'categoryId': geography_df['category_id'],
                            'unitId': geography_df['unit_id'],
                            'data': geography_df['data']})

    print("Total {} records for villagegeography_村庄地理 table".format(len(naturalenv['gazetteerId'])))

    naturalenv.to_csv(output_path + "/villagegeography_村庄地理.csv", index=False, na_rep="NULL")
    geoUnit.to_csv(output_path + "/villagegeographyUnit_村庄地理单位.csv", index=False, na_rep="NULL")

    print("Finish villagegeography_村庄地理.csv")
    print("Finish villagegeographyUnit_村庄地理单位.csv")

    









