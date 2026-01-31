from extras import relPath, getJson, getCSV

# Options

write_output = True

# Read data

file_count = len(list(getJson('../metadata.json')))
country_data = getCSV('../outputs/countries.csv')

data = getCSV(f'../outputs/final.csv')[1:]
country_count = len(data)

data_dict = {i[0]: i[1:] for i in data}

# Sort data

sorted_data = sorted(data, key=(lambda x: float(x[-1])))
sorted_data.reverse()

# Print data

place = 0
total = 0

full_output = ''

for n, item in enumerate(sorted_data):
    warn = '!'

    data_percentage = round(int(item[2]) / file_count * 100)
    code = item[0]

    if data_percentage >= 80: 
        warn = ' '
        place += 1

    value = item[-1][:5]
    total += float(value)

    entry_output = ' '.join((
        warn, 
        str(place).ljust(5), 
        item[1].ljust(45),
        value,
        f'{data_percentage}%'.ljust(7),
        'X' * round(float(value)),
    ))

    full_output += entry_output + '\n'
    
print(full_output.replace('!', '\033[30m!').replace('\n', '\033[0m\n'))

# Write data

if write_output:
    with open(relPath('../outputs/results.txt'), 'w') as f:
        f.write(full_output)


# More stats

print()

average = total / country_count
median = sorted_data[round(country_count / 2)][-1]

print('  Countries:', country_count)
print()

print('  Average:  ', round(average))
print()