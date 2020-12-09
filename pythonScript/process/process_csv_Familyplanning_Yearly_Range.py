import pandas as pd
import math
import sys
from process.validate_csv_data import  check_yearly_records, check_range_records, mapping_id

def create_csv_familyplanning_familyplanningUnit(read_path, output_path, yearly_file, range_file):
    """
    create familyplanning_计划生育.csv, familyplanningUnit_计划生育单位.csv that will be loaded into database.

    Process data in "Family Planning - Range0.csv", "Family Planning - Yearly.csv" files to “familyplanning_计划生育.csv", "familyplanningUnit_计划生育单位.csv”
    Categories for familyplanning table is read from "Database Data" directory
    Categories are predefined and created.
    If categories are changed, familyplanning categories in Category.py should be changed first.

    :param read_path: path to directory contains "Family Planning - Range0.csv", "Family Planning - Yearly.csv"
    :param output_path: path to directory stores "familyplanning_计划生育.csv", "familyplanningUnit_计划生育单位.csv"
    :param yearly_file: file contains familyplanning yearly data
    :param range_file: file contains familyplanning range data
    """
    yearly_df = pd.read_csv(read_path + "/" + yearly_file)
    range_df = pd.read_csv(read_path + "/" + range_file)

    yearly_df = yearly_df.dropna(axis=0, how='all')
    range_df = range_df.dropna(axis=0, how='all')

    yearly_df.drop_duplicates(inplace=True)
    range_df.drop_duplicates(inplace=True)

    # validate data
    print("Validate familyplanning Yearly data")
    correct = check_yearly_records(yearly_df, range(1949, 2020))

    print("Validate familyplanning Range data")
    correct = check_range_records(range_df)

    if not correct:
        sys.exit("Correct records first.")
    else:
        print("Finish validate.")
        
    # create level1 as category
    yearly_df['level1'] = yearly_df['Category']
    
    range_df['level1'] = range_df['Category']

    # add "Unit" column to the yearly_df
    count = 0  # count number of rows
    yearly_df["Unit"] = None  # create a new empty column "Unit"
    yearly_df.head()

    unit_temp = []
    for row in yearly_df['level1'].values.tolist():
        if row == "计划生育率 (%) Planned Birth Rate (%)":
            unit_temp.append("百分比 Percentage")
        elif row == "节育率 (%) Rate of Contraception":
            unit_temp.append("百分比 Percentage")
        elif row == "结扎总数 Total Number of Vasectomies and Tubal Ligations":
            unit_temp.append("人数 Number of People")
        elif row == "领取独生子女证 (人数) Certified Commitment to One Child":
            unit_temp.append("人数 Number of People")
        elif row == "男性结扎 Vasectomies":
            unit_temp.append("人数 Number of People")
        elif row == "女性结扎 Tubal Ligations":
            unit_temp.append("人数 Number of People")
        elif row == "人工流产 Abortions":
            unit_temp.append("人数 Number of People")
        elif row == "上环 Use of Intrauterine Device (IUD)":
            unit_temp.append("人数 Number of People")
        elif row == "引产 Late-term Abortions":
            unit_temp.append("人数 Number of People")
        elif row == "育龄妇女人口 Number of Women of Childbearing Age":
            unit_temp.append("人数 Number of People")
        elif row == "绝育手术 Sterilization Surgeries":
            unit_temp.append("人数 Number of People")
        else:  # set default unit to number of people, should not choose
            unit_temp.append("人数 Number of People")
        count = count + 1
    yearly_df["Unit"] = unit_temp.copy()

    print("added unit column to familyplanning yearly table.")
    #yearly_df.to_csv(output_path + "test.csv",encoding='utf-8-sig')

    # add "Unit" column to the yearly_df
    count = 0  # count number of rows
    range_df["Unit"] = None  # create a new empty column "Unit"
    unit_temp = []
    for row in range_df['level1'].values.tolist():
        if row == "计划生育率 (%) Planned Birth Rate (%)":
            unit_temp.append("百分比 Percentage")
        elif row == "节育率 (%) Rate of Contraception":
            unit_temp.append("百分比 Percentage")
        elif row == "结扎总数 Total Number of Vasectomies and Tubal Ligations":
            unit_temp.append("人数 Number of People")
        elif row == "领取独生子女证 (人数) Certified Commitment to One Child":
            unit_temp.append("人数 Number of People")
        elif row == "男性结扎 Vasectomies":
            unit_temp.append("人数 Number of People")
        elif row == "女性结扎 Tubal Ligations":
            unit_temp.append("人数 Number of People")
        elif row == "人工流产 Abortions":
            unit_temp.append("人数 Number of People")
        elif row == "上环 Use of Intrauterine Device (IUD)":
            unit_temp.append("人数 Number of People")
        elif row == "引产 Late-term Abortions":
            unit_temp.append("人数 Number of People")
        elif row == "育龄妇女人口 Number of Women of Childbearing Age":
            unit_temp.append("人数 Number of People")
        elif row == "绝育手术 Sterilization Surgeries":
            unit_temp.append("人数 Number of People")
        else:  # set default unit to number of people, should not choose
            unit_temp.append("人数 Number of People")
        count = count + 1
    range_df["Unit"] = unit_temp
    print("added unit column to population range_df table.")
    #range_df.to_csv(output_path + "test.csv",encoding='utf-8-sig')

    # transfer yearly_df to dictionary
    yearly_data = {}
    for column in yearly_df.columns:
        yearly_data[column] = yearly_df[column].values.tolist()

    # transfer range_df to dictionary
    range_data = {}
    for column in range_df.columns:
        range_data[column] = range_df[column].values.tolist()

    # merge yearly_df and range_df into df_yearly_range
    yearly_and_range = {
        '村志代码 Gazetteer Code': [],
        'level1': [],
        'Start Year': [],
        'End Year': [],
        'Data': [],
        'Unit': []}

    print("process {} records in {} file".format(len(yearly_data['村志代码 Gazetteer Code']), yearly_file))
    # select and store not null records at yearly
    for i in range(len(yearly_data['村志代码 Gazetteer Code'])):
        for year in range(1949, 2020):
            # skip null records
            if math.isnan(yearly_data[str(year)][i]):
                continue
                # store gazetteer code, categories, unit
            for key in ['村志代码 Gazetteer Code', 'level1', 'Unit']:
                yearly_and_range[key].append(yearly_data[key][i])
            # store data
            yearly_and_range['Data'].append(yearly_data[str(year)][i])
            # store start year, end year
            yearly_and_range['Start Year'].append(year)
            yearly_and_range['End Year'].append(year)

    print("process {} records in {} file".format(len(range_data['村志代码 Gazetteer Code']), range_file))
    # store range records
    for i in range(len(range_data['村志代码 Gazetteer Code'])):
        # store gazetteer code, categories, unit, start year, end year, data
        for key in ['村志代码 Gazetteer Code', 'level1','Start Year', 'End Year', 'Data', 'Unit']:
            yearly_and_range[key].append(range_data[key][i])

    # create df stores yearly and range data
    yearly_and_range_df = pd.DataFrame(yearly_and_range)

    # --- append category id ---
    # group by categories
    groupby_categories = yearly_and_range_df.groupby(['level1'])

    population_df = pd.DataFrame()
    category_df = pd.read_csv("Database data/famliyplanningcategory_计划生育类.csv")

    for group, frame in groupby_categories:
        
        level1_category = group

        parent_id = math.nan
        if level1_category != "":
            category_id = mapping_id(level1_category, parent_id, category_df)
            #parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        population_df = pd.concat([population_df, frame])

    # create unit - id mapping
    units = population_df['Unit'].unique().tolist()
    # df for economyCategory_经济类.csv
    economyUnit = pd.DataFrame({'unit_id': list(range(1, len(units) + 1)), 'name': units})

    # append unit id
    population_df = pd.merge(population_df, economyUnit, left_on='Unit', right_on='name', how='left')

    # df for economy_经济.csv
    economy = pd.DataFrame({'gazetteerId': population_df['村志代码 Gazetteer Code'],
                            'villageInnerId': population_df['村志代码 Gazetteer Code'],
                            'categoryId': population_df['category_id'],
                            'startYear': population_df['Start Year'],
                            'endYear': population_df['End Year'],
                            'unitId': population_df['unit_id'],
                            'data': population_df['Data']})

    economy = economy.astype({'gazetteerId': 'int64', 'villageInnerId':'int64'})

    print("Total {} records for familyplanning_计划生育 table".format(len(economy['gazetteerId'])))

    economy.to_csv(output_path + "/familyplanning_计划生育.csv", index=False, na_rep="NULL")
    economyUnit.to_csv(output_path + "/familyplanningUnit_计划生育单位.csv", index=False, na_rep="NULL")

    print("Finish familyplanning_计划生育.csv")
    print("Finish familyplanningUnit_计划生育单位.csv")