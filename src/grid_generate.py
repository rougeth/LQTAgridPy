from itertools import izip
import matrix_generate

class GridGenerate():

    def __init__(self, x, y, z, dx, dy, dz, atp, fileGro, fileItp):
        coulomb = ""
        lj = ""
        n = len(atp)

        for i in xrange(x):
            for j in xrange(y):
                for k in xrange(z):
                    for l in xrange(n):
                        coulomb += "%d_%d_%d_%s_C \t" % (i+dx, j+dy, k+dz, atp[l])
                        lj += "%d_%d_%d_%s_LJ \t" % (i+dx, j+dy, k+dz, atp[l])

        self.output = coulomb + lj + "\n"
        GMC = matrix_generate.MatrixGenerate(fileGro, fileItp)
        GMC.gridGenerate(x,y,z,atp,dx,dy,dz)
        self.output += "\n" + GMC.saveGrids() + "\n"
    
    def pairwise(iterable):
        a = iter(iterable)
        return izip(a, a)

    def saveGrid(self):
        arq = open("test.txt", "w")
        arq.write(self.output)
        arq.close()
        