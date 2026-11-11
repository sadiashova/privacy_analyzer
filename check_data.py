import csv

with open("data/labels.csv", mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)

headers = rows[0]
data_rows = rows[1:]

print("Column names:")
print(headers)

print("\nNumber of sentences:", len(data_rows))
print("Number of columns:", len(headers))

print("\nDataset:")
for row in data_rows:
    print(row)
