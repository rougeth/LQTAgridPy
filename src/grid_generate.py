from itertools import izip

class gridGenerate():

    def __init__(self, x, y, z, dx, dy, dz, atp, fileName):
        self.output = ""

        n = len(atp)
        for i in xrange(0,x):
            for j in xrange(0,y):
                for k in xrange(0,z):
                    for l in xrange(0,n):
                        self.output = self.output + "%d_%d_%d_%s_C \t" % (i+dx, j+dy, k+dz, atp[l])
                        self.output = self.output + "%d_%d_%d_%s_LJ \t" % (i+dx, j+dy, k+dz, atp[l])

        self.output = self.output + "\n"

            
        with open(fileName) as f:
            self.dataFile = f.readlines()

        for lineGro, lineItp in pairwise(self.dataFile):
            fileNameGro = lineGro
            fileNameItp = lineItp
            GMC = matrixGenerate(fileNameGro, fileNameItp)
            GMC.gridGenerate(x,y,z,atp,dx,dy,dz)
            # output.format(GMC.saveGrids());
            # output.format("\n");
    
    def pairwise(iterable):
        a = iter(iterable)
        return izip(a, a)
        