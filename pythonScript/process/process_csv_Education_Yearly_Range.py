import pandas as pd
import math
import sys
from process.validate_csv_data import check_yearly_records, check_range_records, mapping_id


def create_csv_education_educationUnit(read_path, output_path, yearly_file, range_file):
    """
    create "education_教育.csv", "educationUnit_教育单位.csv" that will be loaded into database.

    Process data in "Education - Yearly.csv", "Education - Range.csv" files to "education_经济.csv", "eduationUnit_经济单位.csv".
    Categories for education table is read from "Database Data" directory's economyCategory_经济类.csv file.
    Categories are predefine and created.
    If categories are changed, economy categories in Category.py should be changed first.

    :param read_path: path to directory contains "Education - Yearly.csv", "Education - Range.csv".
    :param output_path: path to directory stores "education_教育.csv", "educationUnit_教育单位.csv".
    :param yearly_file: file contains education yearly data
    :param range_file: file contains education range data
    """

    print("Processing Education")
    yearly_df = pd.read_csv(read_path + "/" + yearly_file)
    range_df = pd.read_csv(read_path + "/" + range_file)

    # drop all null rows and duplicate rows.
    yearly_df = yearly_df.dropna(axis=0, how='all')
    range_df = range_df.dropna(axis=0, how='all')
    yearly_df.drop_duplicates(inplace=True)
    range_df.drop_duplicates(inplace=True)

    # validate data
    print("Validate Education Yearly data")
    correct = check_yearly_records(yearly_df, range(1949, 2020))

    print("Validate Education Range data")
    correct = check_range_records(range_df)

    if not correct:
        sys.exit("Correct records first.")
    else:
        print("Finish validate")

    # create level1, level2 category
    for column in ['Category', 'Division1']:
        yearly_df[column] = yearly_df[column].where(yearly_df[column].notnull(), "")
        range_df[column] = range_df[column].where(range_df[column].notnull(), "")

    yearly_df['level1'] = yearly_df['Category']
    yearly_df['level2'] = yearly_df['Division1']

    range_df['level1'] = range_df['Category']
    range_df['level2'] = range_df['Division1']

    # transfer yearly_df to dictionary
    yearly_data = {}
    for column in yearly_df.columns:
        yearly_data[column] = yearly_df[column].values.tolist()
    # transfer range_df to dictionary
    range_data = {}
    for column in range_df.columns:
        range_data[column] = range_df[column].values.tolist()

    # merge yearly df and range df into df_yearly_range
    yearly_and_range = {
        '村志代码 Gazetteer Code': [],
        'level1': [],
        'level2': [],
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
            # store gazetteerId, categories
            for key in ['村志代码 Gazetteer Code', 'level1', 'level2']:
                yearly_and_range[key].append(yearly_data[key][i])
            # store data
            yearly_and_range['Data'].append(yearly_data[str(year)][i])
            # store start year, end year
            yearly_and_range['Start Year'].append(year)
            yearly_and_range['End Year'].append(year)
            # store subdivision as unit
            yearly_and_range['Unit'].append(yearly_data['Subdivision'][i])

    print("process {} records in {} file".format(len(range_data['村志代码 Gazetteer Code']), range_file))
    # store range records
    for i in range(len(range_data['村志代码 Gazetteer Code'])):  # each row
        # store gazetteerId, categories, unit, start year, end year, data
        for key in ['村志代码 Gazetteer Code', 'level1', 'level2', 'Start Year', 'End Year', 'Data']:
            yearly_and_range[key].append(range_data[key][i])
        # store subdivision as unit
        yearly_and_range['Unit'].append(range_data['Subdivision'][i])

    # create df stores yeartly and range data
    yearly_and_range_df = pd.DataFrame(yearly_and_range)



    education_df = pd.DataFrame()
    category_df = pd.read_csv("Database data/educationCategory_教育类.csv")
    # group by categories
    groupby_categories = yearly_and_range_df.groupby(['level1', 'level2'])
    for group, frame in groupby_categories:

        level1_category = group[0]
        level2_category = group[1]

        parent_id = math.nan
        if level1_category != "":
            category_id = mapping_id(level1_category, parent_id, category_df)
            parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        if level2_category != "":
            category_id = mapping_id(level2_category, parent_id, category_df)
            parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        education_df = pd.concat([education_df, frame])

    # replace NaN in 'Unit' as 无记录 No record
    education_df['Unit'] = education_df['Unit'].where(education_df['Unit'].notnull(), "无记录 No record")
    # create unit - id mapping
    units = education_df['Unit'].unique().tolist()
    # df for economyCategory_经济类.csv
    educationUnit = pd.DataFrame({'unit_id': list(range(1, len(units) + 1)), 'name': units})
    # append unit id
    education_df = pd.merge(education_df, educationUnit, left_on='Unit', right_on='name', how='left')

    # df for education_教育.csv
    education = pd.DataFrame({'gazetteerId': education_df['村志代码 Gazetteer Code'],
                              'villageInnerId': education_df['村志代码 Gazetteer Code'],
                              'categoryId': education_df['category_id'],
                              'startYear': education_df['Start Year'],
                              'endYear': education_df['End Year'],
                              'unitId': education_df['unit_id'],
                              'data': education_df['Data']})

    print("Total {} records for education_教育 table".format(len(education['gazetteerId'])))

    education.to_csv(output_path + "/education_教育.csv", index=False, na_rep="NULL")
    educationUnit.to_csv(output_path + "/educationUnit_教育单位.csv", index=False, na_rep="NULL")

    print("Finish education_教育.csv")
    print("Finish educationUnit_教育单位.csv")
