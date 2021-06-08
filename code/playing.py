import csv
# This is experimental code


def main():
    with open('../data/Plaas4UListings.csv') as file:
        original_list = csv.DictReader(file)
        big_farm_list = filterBySize(original_list, 30)
        #big_farm_list = filterByPrice(original_list, 15000000)
        for farm in big_farm_list:
            print(farm)


#def convertStringToFloat():
    #price_column = []

def filterBySize(farmList, minimum_size):
    filteredList = []
    for row in farmList:
        size = float(row["Size (ha)"])
        if size >= minimum_size:
            filteredList.append(row)
    return filteredList


#def filterByPrice(farmList, maximum_price):
#    filteredListP =[]
#    for row in farmList:
#       price = float(row["Price (Rand)"])
#       if price <= maximum_price:
#           filteredListP.append(row)
#    return filteredListP


if __name__ == "__main__":
    main()
