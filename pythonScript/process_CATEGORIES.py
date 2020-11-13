import pandas as pd

def dfs_category_dictionary(categories, categories_df, parentId, count):
    """
    dfs predefined predefined hierarchical categories.

    :param categories: each topic's predefined hierarchical categories.
    :param categories_df: dataframe stroes data
    :param parentId: id of parent categories
    :param count: used as id
    :return: final count at current category
    """

    if categories is None:
        return count
    # iterate each category at current level
    for category in categories.keys():
        # process one category
        categories_df['name'].append(category)
        categories_df['id'].append(count)
        if parentId is None:
            categories_df['parentId'].append("NULL")
        else:
            categories_df['parentId'].append(parentId)

        # go to child category, count + 1
        count = dfs_category_dictionary(categories[category], categories_df, count, count + 1)

    # return final count at current level to parent category
    return count

def create_csv_category(CATEGORIES, output_path):
    """
    create csv files for categories table.

    :param CATEGORIES: dictionary contains predefined hierarchical categories.
    """

    for category_table_name in CATEGORIES:

        print("Creat {}.csv".format(category_table_name))
        count = 0
        category_data = {'id': [], 'name': [], 'parentId': []}

        dfs_category_dictionary(CATEGORIES[category_table_name], category_data, None, count + 1)

        categories_df = pd.DataFrame(category_data)
        categories_df.to_csv(output_path + "/{}.csv".format(category_table_name), index=False, na_rep="NULL")
        print("Finished {}.csv for {} table".format(category_table_name,category_table_name))