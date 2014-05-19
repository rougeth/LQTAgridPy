from intertools import izip

class gridGenerate():
    """O construtor dessa classe lê um arquivo com a lista dos arquivos gro e top 
       correspondentes aos resultados das dinâmicas para cada molécula
       e gera o Grid para o conjunto de moléculas"""

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
        