import pandas as pd
import math
import sys
import numpy as np
from process.validate_csv_data import check_yearly_records, check_range_records, mapping_id

def create_csv_natrualenvironment_Unit(read_path, output_path, input_file):
    """
    create natrualenvironment_自然环境.csv, natrualenvironmentUnit_自然环境单位.csv that will be loaded into database.

    Process data in "Natural Environment.csv" file to "natrualenvironment_自然环境.csv", "natrualenvironmentUnit_自然环境单位.csv" 
    Categories for naturalenvironment table is read from "Database Data" directory
    Categories are predefined and created.
    If categories are changed, naturalenvironment categories in Category.py should be changed first.

    :param read_path: path to directory contains "Natural Environment.csv"
    :param output_path: path to directory stores "natrualenvironment_自然环境.csv", "natrualenvironmentUnit_自然环境单位.csv" 
    :param input_file: file contains naturalenvironment data
    """
    df = pd.read_csv(read_path + "/" + input_file)

    df = df.dropna(axis=0, how='all')

    df.drop_duplicates(inplace=True)

    # create the village_inner_id column by directly copying the "村志代码 Gazetteer Code" column
    df["village_inner_id"] = df["村志代码 Gazetteer Code"]

    #---------------csv transpose -------------#
    # subset different column and then combine 3 dataframes together, sort by increasing order of gazetter code
    df1 = df[["村志代码 Gazetteer Code","village_inner_id","海拔 (米) Altitude"]].copy()
    df1.loc[:,"category"] = '海拔 (米) Altitude'
    df1 = df1.rename(columns={'海拔 (米) Altitude':'data'})

    df2 = df[["村志代码 Gazetteer Code","village_inner_id","平均降水量 Average Yearly Precipitation Amount"]].copy()
    df2.loc[:,"category"] = '平均降水量 Average Yearly Precipitation Amount'
    df2 = df2.rename(columns={'平均降水量 Average Yearly Precipitation Amount':'data'})

    df3 = df[["村志代码 Gazetteer Code","village_inner_id","平均温度 Average Yearly Temperature"]].copy()
    df3.loc[:,"category"] = '平均温度 Average Yearly Temperature'
    df3 = df3.rename(columns={'平均温度 Average Yearly Temperature':'data'})

    # combine 3 sub-dataframes to one
    df4 = pd.DataFrame(columns=['村志代码 Gazetteer Code', 'village_inner_id', 'data','category'])
    size = df["村志代码 Gazetteer Code"].count()
    
    count = 0
    for i in range(0, size*3, 3):
        df4.loc[i]=df1.loc[count].tolist()
        df4.loc[i+1]=df2.loc[count].tolist()
        df4.loc[i+2]=df3.loc[count].tolist()
        count+=1

    # create "level1" column using "category" column
    df4['level1'] = df4['category']

    #---------------csv add Unit column -------------#
    count = 0 # count number of rows
    df4["Unit"] = None # create a new empty column "Unit"
    unit_temp = []
    for row in df4['level1'].values.tolist():
        if (row == "海拔 (米) Altitude") and (pd.notna(row)):
            unit_temp.append("米 Meter")
        elif (row == "平均降水量 Average Yearly Precipitation Amount") and (pd.notna(row)):
            unit_temp.append("毫米 millimeter")
        elif (row == "平均温度 Average Yearly Temperature") and (pd.notna(row)):
            unit_temp.append("°C")
        else: # set default unit to number of people
            unit_temp.append("没有相关数据 No Available Data")
    df4["Unit"] = unit_temp
    print("added unit column to natrual environment yearly table.")

    #---------------csv using "natrualenvironmentcategory_自然环境类.csv" to code "category_id" column -------------#
    # group by categories
    groupby_categories = df4.groupby(['level1'])
    
    env_df = pd.DataFrame()
    category_df = pd.read_csv("Database data/naturalenvironmentcategory_自然环境类.csv")

    # add "category_id"
    for group, frame in groupby_categories:
      
        level1_category = group

        parent_id = math.nan
        if level1_category != "":
            category_id = mapping_id(level1_category, parent_id, category_df)
            #parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        env_df = pd.concat([env_df, frame])

    #---------------create "naturalenvironmentUnit.csv" -------------#
    # create unit - id mapping
    units = env_df['Unit'].unique().tolist()
    # df for naturalenvironmentUnit.csv
    envUnit = pd.DataFrame({'unit_id': list(range(1, len(units) + 1)), 'name': units})


    # append unit id
    env_df = pd.merge(env_df, envUnit, left_on='Unit', right_on='name', how='left')

    # df for naturalenvironment_自然环境.csv
    naturalenv = pd.DataFrame({'gazetteerId': env_df['村志代码 Gazetteer Code'],
                            'villageInnerId': env_df['村志代码 Gazetteer Code'],
                            'categoryId': env_df['category_id'],
                            'unitId': env_df['unit_id'],
                            'data': env_df['data']})

    print("Total {} records for naturalenvironment_自然环境 table".format(len(naturalenv['gazetteerId'])))

    naturalenv.to_csv(output_path + "/naturalenvironment_自然环境.csv", index=False, na_rep="NULL")
    envUnit.to_csv(output_path + "/naturalenvironmentUnit_自然环境单位.csv", index=False, na_rep="NULL")

    print("Finish mnaturalenvironment_自然环境.csv")
    print("Finish naturalenvironmentUnit_自然环境单位.csv")





