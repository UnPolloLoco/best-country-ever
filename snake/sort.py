from extras import relPath, getJson, getCSV

data = getCSV(f'../outputs/final.csv')[1:]

sorted_data = sorted(data, key=(lambda x: float(x[-1])))
sorted_data.reverse()

for n, item in enumerate(sorted_data):
    print(
        str(n).ljust(5), 
        item[1].ljust(50),
        item[-1][:5]
    )