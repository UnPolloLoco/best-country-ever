from extras import relPath, getJson, getCSV

# Read data

file_count = len(list(getJson('../metadata.json')))
country_data = getCSV('../outputs/countries.csv')

data = getCSV(f'../outputs/final.csv')[1:]
country_count = len(data)

# Sort data

sorted_data = sorted(data, key=(lambda x: float(x[-1])))
sorted_data.reverse()

# Print data

place = 0
total = 0

for item in sorted_data:
    warn = '\033[30m!'
    data_percentage = round(int(item[2]) / file_count * 100)
    if data_percentage >= 80: 
        warn = ' '
        place += 1

    value = item[-1][:5]
    total += float(value)

    print(
        warn, 
        str(place).ljust(5), 
        item[1].ljust(45),
        value,
        f'{data_percentage}%'.ljust(7),
        'X' * round(float(value)),
        '\033[0m'
    )

# More stats

print()

average = total / country_count
median = sorted_data[round(country_count / 2)][-1]

print('  Countries:', country_count)
print()

print('  Average:  ', round(average))
print()