from Category import CATEGORIES
from process_csv_Village_Information import create_csv_village_and_address, create_csv_city_county_province
from process_CATEGORIES import create_csv_category
from process_csv_Economy_Yearly_Range import create_csv_economy_economyUnit


read_csv_dirct = "All Datasets and Data Dictionary"
output_csv_dirct = "Database Data"

print("---------------")
create_csv_city_county_province(read_csv_dirct, output_csv_dirct, read_file_name="Village Information.csv")

print("---------------")
create_csv_village_and_address(read_csv_dirct, output_csv_dirct, read_file_name="Village Information.csv")

print("---------------")
create_csv_category(CATEGORIES, output_csv_dirct)

print("---------------")
create_csv_economy_economyUnit(read_csv_dirct, output_csv_dirct, yearly_file="Economy - Yearly.csv", range_file="Economy - Range.csv")