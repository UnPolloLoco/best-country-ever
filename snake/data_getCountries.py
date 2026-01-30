from csv import writer
from extras import relPath, getJson, getCSV

# Read metadata

metadata = getJson('../metadata.json')

# Prep country file

csv_file_names = list(metadata)
register = {}
instances = {}

entity_list = register.values()
code_list = register.keys()

# Read CSV data

entity_index = None
code_index = None
data_index = None

next_makeshift_code = 0

for file_name in csv_file_names:
    data = getCSV(f'../data/{file_name}')
    for n, row in enumerate(data):
        is_header = (n == 0)
        if is_header:
            entity_index = row.index('Entity')
            code_index = row.index('Code')
            data_index = row.index(metadata[file_name]['dataHeader'])
        else:
            # Every entry in every file...
            code = row[code_index]
            entity = row[entity_index]

            outcome = None

            if code != '':
                # Code exists
                if code in code_list:
                    # Code registered
                    if register[code] != entity:
                        print(f'Entity does not match ----- {code} {entity} ----- {file_name}')
                    outcome = 'DO NOTHING'
                else:
                    # Code not registered
                    if entity in entity_list:
                        # Entity registered
                        print(f'Entity registered but not code ----- {code} {entity} ----- {file_name}')
                        outcome = 'REGISTER'
                    else:
                        # Entity not registered
                        outcome = 'REGISTER'
            else:
                # Code doesn't exist
                if entity in entity_list:
                    # Entity registered
                    # print(f'No code, but entity registered ----- {code} {entity} ----- {file_name}')
                    outcome = 'DO NOTHING'
                else:
                    # Entity not registered
                    code = next_makeshift_code
                    next_makeshift_code += 1
                    outcome = 'REGISTER'

            # Increment occurance

            if row[data_index] != '':
                if code in instances:
                    instances[code] += 1
                else:
                    instances[code] = 1
            else:
                pass # print(f'Empty data ----- {entity} ----- {file_name}')

            # Update register if needed

            if outcome == 'DO NOTHING':
                pass
            elif outcome == 'REGISTER':
                register[code] = entity





# Write country file

with open(relPath('../outputs/countries.csv'), 'w') as f:
    w = writer(f)
    w.writerow(["Entity", "Code", "Instances"])
    for code in code_list:
        w.writerow([register[code], code, instances[code]])