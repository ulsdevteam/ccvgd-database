import math
import sys
import pandas as pd
from process.validate_csv_data import check_yearly_records, check_range_records, mapping_id


def create_csv_ethnic_ethnicUnit(read_path, output_path, yearly_file, range_file):

    print("Processing Ethnic Groups")
    yearly_df = pd.read_csv(read_path + "/" + yearly_file)
    range_df = pd.read_csv(read_path + "/" + range_file)

    # drop all null rows and duplicate rows.
    yearly_df = yearly_df.dropna(axis=0, how='all')
    range_df = range_df.dropna(axis=0, how='all')
    yearly_df.drop_duplicates(inplace=True)
    range_df.drop_duplicates(inplace=True)

    # validate data
    print("Validate Ethnic Group Yearly data:  ")
    correct = check_yearly_records(yearly_df, range(1949, 2020))

    print("Validate Ethnic Group Range data:   ")
    correct = check_range_records(range_df)

    if not correct:
        sys.exit("Correct records first.")
    else:
        print("Finish validate.")

    # transfer yearly_df to dictionary, for quicker iteration
    yearly_data = {}
    for column in yearly_df.columns:
        yearly_data[column] = yearly_df[column].values.tolist()
    # transfer range_df to dictionary, for quicker iteration
    range_data = {}
    for column in range_df.columns:
        range_data[column] = range_df[column].values.tolist()

    # merge yearly df and range df into df_yearly_range
    yearly_and_range = {
        '村志代码 Gazetteer Code': [],
        '民族 Ethnic Groups': [],
        'Start Year': [],
        'End Year': [],
        'Data': [],
        'Unit': []}

    print("process {} records in {} file".format(len(yearly_data['村志代码 Gazetteer Code']), yearly_file))
    # select and store not null records at yearly
    for i in range(len(yearly_data['村志代码 Gazetteer Code'])):
        for year in range(1949, 2020):
            # store gazetteerId, categories
            for column in ['村志代码 Gazetteer Code', '民族 Ethnic Groups']:
                yearly_and_range[column].append(yearly_data[column][i])
            # store data
            yearly_and_range['Data'].append(yearly_data[str(year)][i])
            # store start year, end year
            yearly_and_range['Start Year'].append(year)
            yearly_and_range['End Year'].append(year)
            # store subdivision as unit
            yearly_and_range['Unit'].append(yearly_data['Division1'][i])

    print("process {} records in {} file".format(len(range_data['村志代码 Gazetteer Code']), range_file))
    # store range records
    for i in range(len(range_data['村志代码 Gazetteer Code'])):  # each row
        # store gazetteerId, categories, unit, start year, end year, data
        for key in ['村志代码 Gazetteer Code', '民族 Ethnic Groups', 'Start Year', 'End Year', 'Data']:
            yearly_and_range[key].append(range_data[key][i])
        # store subdivision as unit
        yearly_and_range['Unit'].append(range_data['Division1'][i])

    # create df stores yeartly and range data
    yearly_and_range_df = pd.DataFrame(yearly_and_range)
    # group by categories
    groupby_categories = yearly_and_range_df.groupby(['民族 Ethnic Groups'])

    # --- append category id ---
    ethnic_df = pd.DataFrame()
    category_df = pd.read_csv("Database data/ethnicGroupsCategory_民族类.csv")

    for group, frame in groupby_categories:
        category = group
        if category != "":
            category_id = mapping_id(category, math.nan, category_df)
            frame['category_id'] = [category_id] * len(frame)

        ethnic_df = pd.concat([ethnic_df, frame])

    # replace NaN in 'Unit' as 无记录 No record
    ethnic_df['Unit'] = ethnic_df['Unit'].where(ethnic_df['Unit'].notnull(), "无记录 No record")
    # create unit - id mapping
    units = ethnic_df['Unit'].unique().tolist()
    # df for ethnicGroup_民族.csv
    ethnicUnit = pd.DataFrame({'unit_id': list(range(1, len(units) + 1)), 'name': units})
    # append unit id
    ethnic_df = pd.merge(ethnic_df, ethnicUnit, left_on='Unit', right_on='name', how='left')

    # df for education_教育.csv
    ethnic = pd.DataFrame({'gazetteerId': ethnic_df['村志代码 Gazetteer Code'],
                           'villageInnerId': ethnic_df['村志代码 Gazetteer Code'],
                           'categoryId': ethnic_df['category_id'],
                           'startYear': ethnic_df['Start Year'],
                           'endYear': ethnic_df['End Year'],
                           'unitId': ethnic_df['unit_id'],
                           'data': ethnic_df['Data']})

    print("Total {} records for ethnicGroups_民族 table".format(len(ethnic['gazetteerId'])))

    ethnic.to_csv(output_path + "/ethnicGroups_民族.csv", index=False, na_rep="NULL")
    ethnicUnit.to_csv(output_path + "/ethnicGroupsUnit_民族单位.csv", index=False, na_rep="NULL")

    print("Finish ethnicGroups_民族.csv")
    print("Finish ethnicGroupsUnit_民族单位.csv")
