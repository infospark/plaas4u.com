import csv
import re


# This is experimental code


def main():
    original_list = get_farms_from_csv()
    farm_list = filter_by_min(original_list)
#    big_farms = filter_by_size(original_list, 30)
#    expensive_and_big_farms = filter_by_price(big_farms, 15000000)
    for farms in farm_list:
        print(farms)
#    for farm in expensive_and_big_farms:
#        print(farm)

def get_farms_from_csv():
    with open('../data/Plaas4UListings.csv') as file:
        original_list = list(csv.DictReader(file))
        return original_list

def extract_float_from_string(string_containing_number):
    return float(re.sub(r'[^.0-9]', "", string_containing_number))

def filter_by_min(farms):
    filtered_list = []
    column_input = input("Which column do you want to filter? ")
    minimum_key = float(input("Please enter the minimum " + column_input + " value: "))
    maximum_key = float(input("Please enter the maximum " + column_input + " value: "))
    for row in farms:
        size = extract_float_from_string(row["Size (ha)"])
        price = extract_float_from_string(row["Price (Rand)"])
        if(size >= minimum_key and size <= maximum_key):
            filtered_list.append(row)
        elif(price >= minimum_key and price <= maximum_key):
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
