from Category import CATEGORIES
import process

read_csv_dirct = "All Datasets and Data Dictionary"
output_csv_dirct = "Database Data"

print("---------------")
process.create_csv_gazetteerInformation(read_csv_dirct, output_csv_dirct, input_file="Gazetteer Information.csv")

print("---------------")
process.create_csv_city_county_province(read_csv_dirct, output_csv_dirct, read_file_name="Village Information.csv")

print("---------------")
process.create_csv_village_and_address(read_csv_dirct, output_csv_dirct, read_file_name="Village Information.csv")

print("---------------")
process.create_csv_category(CATEGORIES, output_csv_dirct)

print("---------------")
process.create_csv_economy_economyUnit(read_csv_dirct, output_csv_dirct, yearly_file="Economy - Yearly.csv", range_file="Economy - Range.csv")

print("---------------")
process.create_csv_education_educationUnit(read_csv_dirct, output_csv_dirct, yearly_file="Education - Yearly.csv", range_file="Education - Range.csv")

print("---------------")
process.create_csv_ethnic_ethnicUnit(read_csv_dirct,output_csv_dirct, yearly_file="Ethnic Groups - Yearly.csv", range_file="Ethnic Groups - Range.csv")
#
print("---------------")
process.create_csv_naturalDisasters(read_csv_dirct, output_csv_dirct, file="Natural Disasters.csv")

print("---------------")
process.create_csv_lastName_lastNameCategory(read_csv_dirct, output_csv_dirct, file="Last Names.csv")

print("---------------")
process.create_csv_population_populationUnit(read_csv_dirct, output_csv_dirct, yearly_file="Population and Migration - Yearly.csv", range_file="Population and Migration - Range.csv")

print("---------------")
process.create_csv_military_militaryUnit(read_csv_dirct, output_csv_dirct, yearly_file="Military, Politics and Management - Yearly.csv", range_file="Military, Politics and Management - Range.csv")

print("---------------")
process.create_csv_familyplanning_familyplanningUnit(read_csv_dirct, output_csv_dirct, yearly_file="Family Planning - Yearly.csv", range_file="Family Planning - Range.csv")

print("---------------")
process.create_csv_natrualenvironment_Unit(read_csv_dirct, output_csv_dirct, input_file = "Natural Environment.csv")

print("---------------")
process.create_csv_villagegeography_Unit(read_csv_dirct, output_csv_dirct, input_file = "Village Information.csv")