import csv
import re


# This is experimental code


def main():
    with open('../data/Plaas4UListings.csv') as file:
        original_list = list(csv.DictReader(file))
        big_farms = filter_by_size(original_list, 30)
        expensive_and_big_farms = filter_by_price(big_farms, 15000000)
        for farm in expensive_and_big_farms:
            print(farm)


def extract_float_from_string(string_containing_number):
    return float(re.sub(r'[^.0-9]', "", string_containing_number))


def filter_by_size(farms, minimum_size):
    filtered_list = []
    for row in farms:
        size = extract_float_from_string(row["Size (ha)"])
        if size >= minimum_size:
            filtered_list.append(row)
    return filtered_list


def filter_by_price(farms, maximum_price):
    filtered_list = []
    for row in farms:
        price = extract_float_from_string(row["Price (Rand)"])
        if price <= maximum_price:
            filtered_list.append(row)
    return filtered_list


if __name__ == "__main__":
    main()
