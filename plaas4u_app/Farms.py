import csv
import re


# This is experimental code


def main():
    original_list = get_farms_from_csv()
    for farms in original_list:
        print(farms)


def get_farms_from_csv():
    with open('../data/Plaas4UListings.csv') as file:
        original_list = list(csv.DictReader(file))
        return original_list

# TODO: Nico, what does the =0 mean after the second parameter?
def extract_float_from_string(param, default_value=0):
    if param is None or param == '':
        return default_value
    if type(param) == int or type(param) == float:
        return param
    else:
        numeric_only = (re.sub(r'[^.0-9]', "", param))
        if len(numeric_only) == 0:
            return default_value
        else:
            return float(re.sub(r'[^.0-9]', "", param))


def filter_by_min_max(farms, column_input, minimum_key, maximum_key):
    filtered_list = []
    for row in farms:
        value = extract_float_from_string(row[column_input])
        if (value >= minimum_key and value <= maximum_key):
            filtered_list.append(row)
    return filtered_list


#def filter_by_size(farms, minimum_size):
#    filtered_list = []
#    for row in farms:
#        size = extract_float_from_string(row["Size (ha)"])
#        if size >= minimum_size:
#            filtered_list.append(row)
#    return filtered_list


#def filter_by_price(farms, maximum_price):
#    filtered_list = []
#    for row in farms:
#        price = extract_float_from_string(row["Price (Rand)"])
#        if price <= maximum_price:
#            filtered_list.append(row)
#    return filtered_list


def sort_by_key(farms, sort_key, reverse_sort=False):
    return sorted(farms, key=lambda farm: extract_float_from_string(farm[sort_key]), reverse=reverse_sort)


if __name__ == "__main__":
    main()
