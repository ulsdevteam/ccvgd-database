import pandas as pd
import math
import sys
from process.validate_csv_data import mapping_id, validate_year_format

def create_csv_naturalDisasters(read_path, output_path, file):
    print("Processing Natural Disasters")
    raw_data = pd.read_csv(read_path + "/" + file)
    raw_data.head()

    # convert df to dictionary, prepare for iteration
    data = {}
    for column in raw_data.columns:
        data[column] = raw_data[column].values.tolist()

    # split single year from records
    data_dict = {
        '村志代码 Gazetteer Code': [],
        '自然灾害种类 Types of Natural Disasters': [],
        '年份 Year': []}
    print("process {} records in {} file".format(len(data['村志代码 Gazetteer Code']), file))
    # for each gazetteer record, split years and store each single year
    for i in range(len(data['村志代码 Gazetteer Code'])):
        years = data['年份 Years'][i].split(',')
        for year in years:
            year = year.strip()
            # skip empty string
            if year == "":
                continue
            data_dict['村志代码 Gazetteer Code'].append(data['村志代码 Gazetteer Code'][i])
            data_dict['自然灾害种类 Types of Natural Disasters'].append(data['自然灾害种类 Types of Natural Disasters'][i])
            data_dict['年份 Year'].append(year.strip())

    print("Validate year format.")
    if not validate_year_format(data_dict):
        sys.exit("Correct records first.")
    else:
        print("Finish Validate.")

    # --- append category id ---
    data_df = pd.DataFrame(data_dict)
    category_df = pd.read_csv("Database data/naturalDisastersCategory_自然灾害类.csv")
    natural_disasters_df = pd.DataFrame()
    # group by categories
    groupby_categories = data_df.groupby(['自然灾害种类 Types of Natural Disasters'])
    # iterate group by results
    for group, frame in groupby_categories:
        category = group
        if category != "":
            category_id = mapping_id(category, math.nan, category_df)
            frame['category_id'] = [category_id] * len(frame)

        natural_disasters_df = pd.concat([natural_disasters_df, frame])
    # natural disasters do not have unit
    # natural disasters for "naturalDisasters_自然灾害.csv"
    natural_disasters = pd.DataFrame({'gazetteerId': natural_disasters_df['村志代码 Gazetteer Code'],
                                      'villageInnerId': natural_disasters_df['村志代码 Gazetteer Code'],
                                      'categoryId': natural_disasters_df['category_id'],
                                      'year': natural_disasters_df['年份 Year']})

    natural_disasters.to_csv(output_path + "/naturalDisasters_自然灾害.csv", index=False, na_rep="NULL")

    print("Total {} records for naturalDisasters_自然灾害 table".format(len(natural_disasters['gazetteerId'])))
    print("Finish naturalDisasters_自然灾害.csv")

