from extras import relPath, getJson, getCSV

with open(relPath('../mapping/worldMap.svg'), 'r') as f:
    print(f.readline())
    print(f.readline())
    print(f.readline())