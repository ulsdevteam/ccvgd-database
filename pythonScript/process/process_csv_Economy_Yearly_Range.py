import pandas as pd
import math
import sys
from process.validate_csv_data import check_yearly_records, check_range_records, mapping_id


def create_csv_economy_economyUnit(read_path, output_path, yearly_file, range_file):
    """
    create economy_经济.csv, economyUnit_经济单位.csv that will be loaded into database.

    Process data in "Economy - Yearly.csv", "Economy - Range.csv" files to "economy_经济.csv", "economyUnit_经济单位.csv"
    Categories for economy table is read from "Database Data" directory
    Categories are predefine and created.
    If categories are changed, economy categories in Category.py should be changed first.

    :param read_path: path to directory contains "Economy - Yearly.csv", "Economy - Range.csv"
    :param output_path: path to directory stores "economy_经济.csv", "economyUnit_经济单位.csv"
    :param yearly_file: file contains economy yearly data
    :param range_file: file contains economy range data
    """
    yearly_df = pd.read_csv(read_path + "/" + yearly_file)
    range_df = pd.read_csv(read_path + "/" + range_file)

    yearly_df = yearly_df.dropna(axis=0, how='all')
    range_df = range_df.dropna(axis=0, how='all')

    yearly_df.drop_duplicates(inplace=True)
    range_df.drop_duplicates(inplace=True)

    # validate data
    print("Validate Economy Yearly data")
    correct = check_yearly_records(yearly_df, range(1949, 2020))

    print("Validate Economy Range data")
    correct = check_range_records(range_df)

    if not correct:
        sys.exit("Correct records first.")
    else:
        print("Finish validate.")

    # create level1, level2, and level3 category
    for column in ['Division1', 'Division2', 'Subdivision - Agri.', 'Subdivision - Misc.', 'Subdivision - Service','Subdivision - Household']:
        yearly_df[column] = yearly_df[column].where(yearly_df[column].notnull(), "")
        range_df[column] = range_df[column].where(range_df[column].notnull(), "")

    yearly_df['level1'] = yearly_df['Category']
    yearly_df['level2'] = yearly_df['Division1'] + yearly_df['Division2']
    yearly_df['level3'] = yearly_df['Subdivision - Agri.'] + yearly_df['Subdivision - Misc.'] + yearly_df[
        'Subdivision - Service'] + yearly_df['Subdivision - Household']

    range_df['level1'] = range_df['Category']
    range_df['level2'] = range_df['Division1'] + range_df['Division2']
    range_df['level3'] = range_df['Subdivision - Agri.'] + range_df['Subdivision - Misc.'] + range_df[
        'Subdivision - Service'] + range_df['Subdivision - Household']

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
        'level2': [],
        'level3': [],
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
            for key in ['村志代码 Gazetteer Code', 'level1', 'level2', 'level3', 'Unit']:
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
        for key in ['村志代码 Gazetteer Code', 'level1', 'level2', 'level3', 'Start Year', 'End Year', 'Data', 'Unit']:
            yearly_and_range[key].append(range_data[key][i])

    # create df stores yearly and range data
    yearly_and_range_df = pd.DataFrame(yearly_and_range)

    # --- append category id ---
    # group by categories
    groupby_categories = yearly_and_range_df.groupby(['level1', 'level2', 'level3'])

    economy_df = pd.DataFrame()
    category_df = pd.read_csv("Database data/economyCategory_经济类.csv")

    for group, frame in groupby_categories:

        level1_category = group[0]
        level2_category = group[1]
        level3_category = group[2]

        parent_id = math.nan
        if level1_category != "":
            category_id = mapping_id(level1_category, parent_id, category_df)
            parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        if level2_category != "":
            category_id = mapping_id(level2_category, parent_id, category_df)
            parent_id = category_id
            frame['category_id'] = [category_id] * len(frame)

        if level3_category != "":
            category_id = mapping_id(level3_category, parent_id, category_df)
            frame['category_id'] = [category_id] * len(frame)

        economy_df = pd.concat([economy_df, frame])

    # create unit - id mapping
    units = economy_df['Unit'].unique().tolist()
    # df for economyCategory_经济类.csv
    economyUnit = pd.DataFrame({'unit_id': list(range(1, len(units) + 1)), 'name': units})

    # append unit id
    economy_df = pd.merge(economy_df, economyUnit, left_on='Unit', right_on='name', how='left')

    # df for economy_经济.csv
    economy = pd.DataFrame({'gazetteerId': economy_df['村志代码 Gazetteer Code'],
                            'villageInnerId': economy_df['村志代码 Gazetteer Code'],
                            'categoryId': economy_df['category_id'],
                            'startYear': economy_df['Start Year'],
                            'endYear': economy_df['End Year'],
                            'unitId': economy_df['unit_id'],
                            'data': economy_df['Data']})

    print("Total {} records for economy_经济 table".format(len(economy['gazetteerId'])))

    economy.to_csv(output_path + "/economy_经济.csv", index=False, na_rep="NULL")
    economyUnit.to_csv(output_path + "/economyUnit_经济单位.csv", index=False, na_rep="NULL")

    print("Finish economy_经济.csv")
    print("Finish economyUnit_经济单位.csv")
