from csv import writer
from extras import relPath, getJson, getCSV, interpolate

# Read necesary files

metadata = getJson('../metadata.json')
data = getCSV('../outputs/allData.csv')

# Setup

output_headers = ['Code', 'Entity', 'Instances', 'Value']
input_headers = []
final_value_dict = {}

# Data collection


for row_num, row in enumerate(data):
    if row_num == 0:
        input_headers = row
    else:
        # Every row...
        code = row[0]
        entity = row[1]
        instances = row[2]

        total_weight = 0
        weighted_value = 0

        for n, value in enumerate(row):
            # Every datapoint in every row...
            if n > 2:
                category = input_headers[n]

                if value == '': continue
                value = float(value)

                # Normalize value

                normalized_value = None
                upper_bound_index = None
                value_mapper = metadata[category]['values']

                for m_num, m in enumerate(value_mapper):
                    if m['in'] >= value:
                        upper_bound_index = m_num
                        break

                if upper_bound_index == None:
                    upper_bound_index = len(value_mapper) - 1
                
                in_lower = value_mapper[upper_bound_index - 1]['in']
                in_upper = value_mapper[upper_bound_index]['in']
                out_lower = value_mapper[upper_bound_index - 1]['out']
                out_upper = value_mapper[upper_bound_index]['out']

                normalized_value = interpolate(
                    value,
                    in_lower, in_upper,
                    out_lower, out_upper
                )

                # Manage weighting

                weight = metadata[category]['weight']

                total_weight += weight
                weighted_value += normalized_value * weight

        # Finalize row

        final_value = weighted_value / total_weight * 100
        final_value_dict[code] = final_value

# Build the file

with open(relPath('../outputs/final.csv'), 'w') as f:
    w = writer(f)
    w.writerow(output_headers)
    for row in data[1:]:
        w.writerow([
            row[0],
            row[1],
            row[2],
            final_value_dict[row[0]]
        ])