import math

class matrixGenerate():

    def __init__(self, fileGro, fileItp):
        # determinaX(arquivogro);
        # tiposdeatomos(arquivoitp);
        # carregaConstantes();
        # carregaAP();
        # determinaConstantes();
        
    def gridGenerate(I, J, K, atp, dx, dy, dz):
        f = 138.935485
        nframes = self.m / self.n
        natp = len(atp)
        self.gridCoulomb = [[[[0 for x in xrange(I)] for x in xrange(J)] for x in xrange(K)] for x in xrange(natp)]
        self.gridLJ = [[[[0 for x in xrange(I)] for x in xrange(J)] for x in xrange(K)] for x in xrange(natp)]

        for h in xrange(0, natp):
            elem = search(self.ap, atp[h])
            q1 = self.cargasap[elem]
            c6a = self.c6ap[elem]
            c12a = self.c12ap[elem]

            npontos = 0
            r1 = []

            for i in xrange(0,I):
                r1.insert(0, i + dx)
                for j in xrange(0,J):
                    r1.insert(1, j + dy)
                    for k in xrange(0,K):
                        r1.insert(2, k + dz)

                        Vlj = 0
                        Vc = 0
                        ++npontos

                        for l in xrange(0,self.m):
                            r = distance(r1, self.X[l]) / 10
                            index = l % self.n
                            c6ij = math.sqrt(c6a * self.c6[index])
                            c12ij = math.sqrt(c12a * self.c12[index])
                            Vlj = Vlj + (c12ij / (math.pow(r, 12))) - (c6ij / (math.pow(r, 6)))
                            Vc = Vc + f * q1 * self.cargos[index] / r

                        self.gridCoulomb[i][j][k][h] = Vc / nframes
                        self.gridLJ[i][j][k][h] = Vlj / math.sqrt(nframes)

    def saveGrids():
        output = ""

        I = len(self.gridCoulomb)
        J = len(self.gridCoulomb[0])
        K = len(self.gridCoulomb[0][0])
        L = len(self.gridCoulomb[0][0][0])
        
        for i in xrange(0,I):
            for j in xrange(0,J):
                for k in xrange(0,K):
                    for l in xrange(0,L):
                        # saida.format("%-15g\t", self.gridCoulomb[i][j][k][l]);
                        # saida.format("%-15g\t", self.gridLJ[i][j][k][l]);
        return output
    