import csv
# This is experimental code

def main():
    filteredList = []
    with open('../data/Plaas4UListings.csv') as file:
        reader = csv.DictReader(file)
        for row in reader:
            size = float(row["Size (ha)"])
            if size >= 30:
                filteredList.append(row)
    print(filteredList)


if __name__ == "__main__":
    main()
