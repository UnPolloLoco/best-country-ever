from pathlib import Path
from json import loads as loadJSON
from csv import reader as readCSV

def relPath(path): return (str(Path(__file__).parent) + '/' + path)

def getJson(path): 
    with open(relPath(path), 'r') as file:
        return loadJSON(file.read())

def getCSV(path):
    with open(relPath(path), 'r') as file:
        reader = readCSV(file)
        output = []
        for i in reader:
            output.append(i)
        return output

def interpolate(x, a1, a2, b1, b2):
    return (b2 - b1) * (x - a1) / (a2 - a1) + b1