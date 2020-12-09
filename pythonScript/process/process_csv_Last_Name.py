import pandas as pd


def create_csv_lastName_lastNameCategory(read_path, output_path, file):

    print("Processing Last Names")
    raw_data = pd.read_csv(read_path + "/" + file)

    # split names and pinyins columns
    raw_data.columns = ['gazetteer code', 'gazetteer title', 'total number', 'five last names', 'pinyins']
    name_columns = ['first last name', 'second last name', 'third last name', 'fourth last name', 'fifth last name']
    pinyin_columns = ['first pinyin', 'second pinyin', 'third pinyin', 'fourth pinyin', 'fifth pinyin']
    raw_data[name_columns + ['tail name']] = raw_data['five last names'].str.split(', ', expand=True)
    raw_data[pinyin_columns + ['tail pinyin']] = raw_data['pinyins'].str.split(', ', expand=True)

    # replace NaN, 'nan', 'n/a' as None
    for column in name_columns:
        raw_data[column] = raw_data[column].where(raw_data[column].notnull(), None)
        raw_data[column] = raw_data[column].where(raw_data[column] != 'nan', None)
        raw_data[column] = raw_data[column].where(raw_data[column] != 'n/a', None)
    for column in pinyin_columns:
        raw_data[column] = raw_data[column].where(raw_data[column].notnull(), None)
        raw_data[column] = raw_data[column].where(raw_data[column] != 'nan', None)
        raw_data[column] = raw_data[column].where(raw_data[column] != 'n/a', None)
    # format to single name format
    data = pd.DataFrame()
    for column in ['gazetteer code', 'total number'] + name_columns:
        data[column] = raw_data[column].values.tolist()

    # create id for name
    names = []
    pinyins = []
    for column in name_columns:
        names = names + raw_data[column].values.tolist()
    for column in pinyin_columns:
        pinyins = pinyins + raw_data[column].values.tolist()

    id_name_pinyin = {'id': [], 'name': [], 'pinyin': []}
    code = 0
    for name, pinyin in zip(names, pinyins):
        if (name not in id_name_pinyin['name']) and (name is not None):
            code = code + 1
            id_name_pinyin['id'].append(code)
            id_name_pinyin['name'].append(name)
            id_name_pinyin['pinyin'].append(pinyin)

    last_name_categories = pd.DataFrame({'id': id_name_pinyin['id'],
                                         'name': id_name_pinyin['name'],
                                         'pinyin': id_name_pinyin['pinyin']})

    last_name = pd.DataFrame(columns=['gazetteer code',
                                      'village inner id',
                                      'first last name id',
                                      'second last name id',
                                      'third last name id',
                                      'fourth last name id',
                                      'fifth last name id',
                                      'total number'])

    last_name['gazetteer code'] = data['gazetteer code']
    last_name['village inner id'] = data['gazetteer code']

    df = pd.merge(data, last_name_categories, left_on="first last name", right_on="name", how="left")
    last_name['first last name id'] = df['id']

    df = pd.merge(data, last_name_categories, left_on="second last name", right_on="name", how="left")
    last_name['second last name id'] = df['id']

    df = pd.merge(data, last_name_categories, left_on="third last name", right_on="name", how="left")
    last_name['third last name id'] = df['id']

    df = pd.merge(data, last_name_categories, left_on="fourth last name", right_on="name", how="left")
    last_name['fourth last name id'] = df['id']

    df = pd.merge(data, last_name_categories, left_on="fifth last name", right_on="name", how="left")
    last_name['fifth last name id'] = df['id']

    last_name['total number'] = data['total number']

    # replace "NaN" as None
    last_name = last_name.where(last_name.notnull(), None)

    print("Total {} records for lastName_姓氏 table".format(len(last_name['gazetteer code'])))
    last_name.to_csv(output_path + "/lastName_姓氏.csv", index=False, na_rep="NULL")
    last_name_categories.to_csv(output_path + "/lastNameCategory_姓氏类别.csv", index=False, na_rep="NULL")

    print("Finish lastName_姓氏.csv")
    print("Finish lastNameCategory_姓氏类别.csv")















