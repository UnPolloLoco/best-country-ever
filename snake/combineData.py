from csv import writer
from extras import relPath, getJson, getCSV

# Read necesary files

metadata = getJson('../metadata.json')
country_data = getCSV('../outputs/countries.csv')

file_names = list(metadata)

entity_list = [i[0] for i in country_data[1:]]
code_list = [i[1] for i in country_data[1:]]

# Setup

output_headers = ['Code', 'Entity', 'Instances'] + file_names
data_dict = {}

for i in range(len(code_list)):
    data_dict[code_list[i]] = [entity_list[i], 0] + ['' for f in file_names]

# Add data

for file in file_names:
    data = getCSV(f'../data/{file}')
    
    # Subtract 1 to account for CODE temporarily being a key and not a value
    value_destination_index = output_headers.index(file) - 1 

    for n, row in enumerate(data):
        is_header = (n == 0)
        if is_header:
            entity_index = row.index('Entity')
            code_index = row.index('Code')
            data_index = row.index(metadata[file]['dataHeader'])
        else:
            # Every entry in every file...
            entity = row[entity_index]
            code = row[code_index]
            value = row[data_index]

            if code == '':
                code = code_list[entity_list.index(entity)]
        
            data_dict[code][value_destination_index] = value

            if value != '': data_dict[code][1] += 1 # Increment instance counter

# Finalize and export data

final_data = [([i] + data_dict[i]) for i in data_dict] # Convert from dict to CSV-friendly list

with open(relPath('../outputs/allData.csv'), 'w') as f:
    w = writer(f)
    w.writerow(output_headers)
    for row in final_data:
        w.writerow(row)