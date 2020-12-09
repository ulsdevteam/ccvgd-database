import pandas as pd

def create_csv_gazetteerInformation(read_path, output_path, input_file):
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

    print("Processing Gazetteer Information")
    df = pd.read_csv(read_path + "/" + input_file)

    print("Total {} records for gazetteerInformation_村志信息 table".format(len(df['村志代码 Gazetteer Code'])))

    df.to_csv(output_path + "/gazetteerInformation_村志信息.csv", index=False, na_rep="NULL")