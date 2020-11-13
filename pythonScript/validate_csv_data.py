import math
from datetime import datetime

def data_is_number_or_nan(record):
    try:
        float(record)
    except:
        return False
    else:
        return True


def iterate_gazetteers_records(gazetteers, records, start_years, end_years):
    correct = True

    for (gazetteer, data, start_year, end_year) in zip(gazetteers, records, start_years, end_years):
        if not data_is_number_or_nan(data):
            correct = False
            print("   record {} at gazetteer {}'s {}-{} is not a number".format(data, gazetteer, start_year, end_year))

    return correct


def check_yearly_records(df, years):
    correct = True

    gazetteers = df['村志代码 Gazetteer Code'].values.tolist()
    for year in years:
        records = df[str(year)].values.tolist()
        start_years = [str(year)] * len(records)
        end_years = [str(year)] * len(records)
        correct = iterate_gazetteers_records(gazetteers, records, start_years, end_years)

    return correct


def check_range_records(df):
    correct = True

    gazetteers = df['村志代码 Gazetteer Code'].values.tolist()
    records = df['Data'].values.tolist()
    start_years = df['Start Year'].values.tolist()
    end_years = df['End Year'].values.tolist()

    correct = iterate_gazetteers_records(gazetteers, records, start_years, end_years)

    return correct

def validate_year_format(natural_disasters):

    valid = True

    for (gazetteer, year) in zip(natural_disasters['村志代码 Gazetteer Code'], natural_disasters['年份 Year']):
        try:
            datetime.strptime(year, "%Y")
        except ValueError:
            print("Invalid year records {} at gazetteer {}.".format(year, gazetteer))
            valid = False

    return valid

def mapping_id(category, parent_id, df):
    if math.isnan(parent_id):
        category = df[df['name'] == category]
        category_id = category['id'].values[0]
        return category_id
    else:
        category = df[(df['name'] == category) & (df['parentId'] == parent_id)]
        category_id = category['id'].values[0]
        return category_id
