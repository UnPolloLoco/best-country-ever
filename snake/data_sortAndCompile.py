from extras import relPath, getJson, getCSV
from csv import writer

# Options

print_data = False

# Read data

data_file_names = list(getJson('../metadata.json'))
file_count = len(data_file_names)

country_data = getCSV('../outputs/countries.csv')

data = getCSV(f'../outputs/final.csv')[1:]
country_count = len(data)

data_dict = {i[0]: i[1:] for i in data}

# Sort data

sorted_data = sorted(data, key=(lambda x: float(x[-1])))
sorted_data.reverse()

# Print data

place = 0
true_place = 0
total = 0

full_output = ''

for n, item in enumerate(sorted_data):
    warn = '!'

    data_percentage = (int(item[2]) / file_count * 100)
    code = item[0]

    if data_percentage >= 80: 
        warn = ' '
        place += 1

    true_place += 1

    value = item[-1][:5]
    total += float(value)
    
    # Add placement to sorted data
    sorted_data[n].append(place)
    sorted_data[n].append(true_place)
    sorted_data[n].append(data_percentage)

    entry_output = ' '.join((
        warn, 
        str(place).ljust(5), 
        item[1].ljust(45),
        value,
        f'{round(data_percentage)}%'.ljust(7),
        'X' * round(float(value)),
    ))

    full_output += entry_output + '\n'
    
if print_data: 
    print(full_output.replace('!', '\033[30m!').replace('\n', '\033[0m\n'))

    # More stats

    print()

    average = total / country_count
    median = sorted_data[round(country_count / 2)][-2]

    print('  Countries:', country_count)
    print()
    print('  Average:  ', round(average))
    print()

# Get additional data

all_data_csv = getCSV('../outputs/allData.csv')
all_data_dict = {i[0]: i for i in all_data_csv}

sorted_dict = {i[0]: i for i in sorted_data}

# Write placement text file

with open(relPath('../outputs/results.txt'), 'w') as f:
    f.write(full_output)

# Write megafile

output_headers = ['Code', 'Rank', 'True Rank', 'Entity', 'Instances', 'Accuracy', 'Value'] + data_file_names

with open(relPath('../outputs/finalDetailed.csv'), 'w') as f:
    w = writer(f)
    for n, code in enumerate(all_data_dict):
        if n == 0:
            # Header row
            w.writerow(output_headers)
        else:
            # Data rows
            ad = all_data_dict[code]
            so = sorted_dict[code]

            this_row = [
                code,           # Code
                so[4],          # Rank
                so[5],          # True Rank
                ad[1],          # Entity
                ad[2],          # Instances
                so[6],          # Accuracy
                so[3],          # Value
            ]

            this_row += ad[3:]  # All data points

            w.writerow(this_row)