from extras import relPath, getJson, getCSV

# Options

show_map = True

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

for n, item in enumerate(sorted_data):
    warn = '\033[30m!'

    data_percentage = round(int(item[2]) / file_count * 100)
    code = item[0]

    if data_percentage >= 80: 
        warn = ' '
        place += 1

    value = item[-1][:5]
    total += float(value)

    if show_map:
        if n < 3 or n >= len(sorted_data) - 3 or code == 'USA':
            if code == 'USA': warn = '>'
            print(
                warn, 
                str(place).ljust(5), 
                item[1].ljust(45),
                value,
                f'{data_percentage}%'.ljust(7),
                '\033[0m'
            )
    
    else:
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

if not show_map:
    print('  Countries:', country_count)
    print()

    print('  Average:  ', round(average))
    print()

# Mapping

if show_map:
    # Get/sort mapping data

    coords = getCSV('../otherData/coords.csv')[1:]

    sorted_coords = sorted(coords, key=(lambda x: float(x[-2])))
    sorted_coords.reverse()

    # Make lat dict

    latitude_dict = {i: [] for i in range(-90, 90)}
    for i in sorted_coords:
        lat = round(float(i[-2]))
        latitude_dict[lat].append(i)

    # Sort lat dict by lon

    for i in latitude_dict:
        sorted_lon = sorted(latitude_dict[i], key=(lambda x: float(x[-1])))
        latitude_dict[i] = sorted_lon

    # Map generator

    full_map = {}

    for lat in range(-90, 90):
        full_map[lat] = {}
        lat_data = latitude_dict[lat]

        item_on_lat = 0
        
        for lon in range(-180, 180):
            full_map[lat][lon] = [-1, None]

            if item_on_lat + 1 <= len(lat_data):
                # If there exists any remaining countries on this latitude...

                item = latitude_dict[lat][item_on_lat]

                if round(float(item[-1])) == lon:
                    item_on_lat += 1
                    full_map[lat][lon] = [0, item[1]]

    # Map drawer

    for lat in range(89, -91, -1):
        line = ''
        for lon in range(-180, 180):
            if full_map[lat][lon][0] == -1:
                line += '  '
            else:
                code = full_map[lat][lon][1]

                if code in data_dict:
                    value = float(data_dict[code][-1])
                    if value > 60:
                        line += 'XX'
                    else:
                        line += '..'
                else:
                    line += '. '
        
        print(line)