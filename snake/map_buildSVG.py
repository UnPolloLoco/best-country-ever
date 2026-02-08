from extras import relPath, getJson, getCSV

# Read SVG

svg = []

with open(relPath('../mapping/worldMap.svg')) as file:
    for line in file:
        svg.append(line.strip())

# Delete lines that start with a certain string

new_svg = []
forbidden_starters = [
    '<?xml',
    '<defs',
    '<sodipodi:namedview',
    '<text id=',
    '<text xml:space=',
    '<rect id="selection-rectangle"'
]

for line in svg:
    keepLine = True
    for x in forbidden_starters:
        if line[:len(x)] == x:
            keepLine = False
            
    if keepLine: new_svg.append(line)

# Prepare entity/code converter

country_csv = getCSV('../outputs/countries.csv')
entity_to_code = {i[0]: i[1] for i in country_csv}

character_replacers = {
    '_': ' ',
    'ã': 'a',
    'é': 'e',
    'ü': 'u',
}
name_replacers = {
    'Cabo Verde':       'Cape Verde',
    'Turkiye':          'Turkey',
    'DR Congo':         'Democratic Republic of Congo',
    'Cote d Ivoire':    "Cote d'Ivoire",
    'Timor Leste':      'East Timor',
    'Guinea Bissau':    'Guinea-Bissau',
    'Palestinian Territories': 'Palestine',
}

# Load big data

data_csv = getCSV('../outputs/finalDetailed.csv')
data_dict = {i[0]: i for i in data_csv}


# Condense data

svg = new_svg
new_svg_string = ''

for line in svg:
    new_text = ''
    
    if line.startswith('<g id="g'):
        # Country group opening tag
        new_text = '<g>'

    elif line.startswith('</svg>'):
        # Last line
        new_text = '<use id="z-index-override" href="#USA"/>' + '\n' + line + '\n'

    elif line.startswith('<path id'):
        # Start of country data ----------------------------------------------------------------------------------------------------------
        name_start = line.index('"')
        name_end = line.index('"', name_start+1)
        name = line[name_start+1 : name_end]
        code = ''

        path_start = line.index(' d=') + 3
        path_end = line.index('"', path_start+1)
        path = line[path_start+1 : path_end]

        # Find code

        cleansed_name = name
        for x in character_replacers:
            cleansed_name = cleansed_name.replace(x, character_replacers[x])

        if cleansed_name in entity_to_code:
            # Convert country name to CODE
            code = entity_to_code[cleansed_name]
        elif cleansed_name in name_replacers:
            # Use alias to convert name to CODE
            cleansed_name = name_replacers[cleansed_name]
            code = entity_to_code[cleansed_name]
        else: 
            # Complain that there is no known CODE
            print(name, "doesn't have a code!!")
            code = name

        code_exists = (code != name)

        # Get country's values

        country_data = []

        if code_exists:
            country_data = data_dict[code]
            data_string = ','.join(country_data)
        else:
            # All empty, save for the entity name
            data_string = ',' * 3
            data_string += cleansed_name
            data_string += ',' * (len(data_dict['USA']) - 1 - 3)

        # Bonus class

        bonus_class = ''
        data_accuracy = 0

        print(country_data)
        
        if code_exists:
            data_accuracy = float(country_data[5])

        if data_accuracy < 80:
            bonus_class = ' low-data'
        if data_accuracy == 0:
            bonus_class = ' no-data'

        # Add the text

        new_text = f'<path class="country-path{bonus_class}" id="{code}" data-stats="{data_string}" d="{path}"></path>'

        # End of country data ----------------------------------------------------------------------------------------------------------

    else:
        # All other lines
        new_text = line + '\n'

    new_svg_string += new_text

# Write improved SVG

with open(relPath('../outputs/betterMap.svg'), 'w') as f:
    f.write(new_svg_string)