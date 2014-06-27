import grid_generate
import sys

# Here are read input files
args = sys.argv[1:]

def main(fileGro, fileItp):
    x = 3
    y = 3
    z = 3
    dx = 3
    dy = 3
    dz = 3
    atp = ["q","a","q","c","a","c","x","c","q","a","x","q","c","q","q","a",]
    
    grid = grid_generate.GridGenerate(x, y, z, dx, dy, dz, atp, fileGro, fileItp)
    grid.saveGrid("test.txt")

main(args[0], args[1])
