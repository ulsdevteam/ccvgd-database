import csv


def read_csv_file(path):
    """
    Read csv file that can be directly inserted into table.

    In ccvg database these csv files should be predefined categories, units, province, city, county
    Header and data of csv file are reading separately.

    :param path: path to csv file
    :return: data: records will be directly inserted into database
             csv_header: head of csv file
    """
    data = []
    csv_header = ""
    read_header = True
    with open(path, encoding="utf-8", mode="r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if read_header:
                csv_header = row
                read_header = False
                continue
            # replace string "NULL" with None type
            new_row = [None if item == "NULL" else item for item in row]
            data.append(tuple(new_row))

    return data, csv_header


def write_csv_file(path, file_name, csv_header, incorrect_records):
    # write records that didn't be successfully inserted into table.
    path_to_file = path + "/" + file_name + ".csv"
    with open(path_to_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(incorrect_records)
    print("Finish writing incorrect records for {} at {} directory.".format(file_name, path))
