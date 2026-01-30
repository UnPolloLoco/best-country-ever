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

        data_start = line.index(' d=') + 3
        data_end = line.index('"', data_start+1)
        data = line[data_start+1 : data_end]

        new_text = f'<path id="{name}" d="{data}"></path>'

    else:
        new_text = line + '\n'

    new_svg_string += new_text



# Write compressed SVG

with open(relPath('../outputs/compressedMap.svg'), 'w') as f:
    f.write(new_svg_string)
    # for line in new_svg:
    #     f.write(line + '\n')