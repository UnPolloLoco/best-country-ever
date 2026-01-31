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

# Prepare score-getter and instances-getter

final_csv = getCSV('../outputs/final.csv')
code_to_score = {i[0]: i[3] for i in final_csv}
code_to_instances = {i[0]: i[2] for i in final_csv}

max_instances = len(list(getJson('../metadata.json')))

# Condense data

svg = new_svg
new_svg_string = ''

for line in svg:
    new_text = ''
    
    if line.startswith('<g id="g'):
        # Country group opening tag
        new_text = '<g>'

    elif line.startswith('<path id'):
        # Country data
        name_start = line.index('"')
        name_end = line.index('"', name_start+1)
        name = line[name_start+1 : name_end]
        code = ''

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

        data_start = line.index(' d=') + 3
        data_end = line.index('"', data_start+1)
        data = line[data_start+1 : data_end]

            # Get country's values

        score = 0
        instances = 0
        if code in code_to_score:
            score = code_to_score[code]
            instances = code_to_instances[code]

            # Bonus class

        bonus_class = ''

        if int(instances) / max_instances < 0.8:
            bonus_class = ' low-data'

        if instances == 0:
            bonus_class = ' no-data'

            # Add the text
        new_text = f'<path class="country-path{bonus_class}" id="{code}" data-score="{score}" d="{data}"></path>'

    else:
        # All other lines
        new_text = line + '\n'

    new_svg_string += new_text

# Write improved SVG

with open(relPath('../outputs/betterMap.svg'), 'w') as f:
    f.write(new_svg_string)