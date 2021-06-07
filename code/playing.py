import csv
# This is experimental code


def main():
    with open('../data/Plaas4UListings.csv') as file:
        original_list = csv.DictReader(file)
        big_farm_list = filterBySize(original_list, 30)
        for farm in big_farm_list:
            print(farm)


def filterBySize(farmList, minimum_size):
    filteredList = []
    for row in farmList:
        size = float(row["Size (ha)"])
        if size >= minimum_size:
            filteredList.append(row)
    return filteredList


if __name__ == "__main__":
    main()
