import grid_generate
import sys
import re

# Here are read input files
args = sys.argv[1:]

def main(fileGro, fileItp, coordinates, dimensions, atp):
    coordinates = re.findall(r"[\w\.\-\+\(\)\=']+", coordinates)
    dimensions = re.findall(r"[\w\.\-\+\(\)\=']+", dimensions)
    atp = re.findall(r"[\w\.\-\+\(\)\=']+", atp)

    x,y,z = int(coordinates[0]), int(coordinates[1]), int(coordinates[2])
    dx, dy, dz = int(dimensions[0]), int(dimensions[1]), int(dimensions[2])
    
    grid = grid_generate.GridGenerate(x, y, z, dx, dy, dz, atp, fileGro, fileItp)
    grid.saveGrid()

main(args[0], args[1], args[2], args[3], args[4])
