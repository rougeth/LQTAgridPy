import math
import re

class MatrixGenerate():

    def __init__(self, fileGro, fileItp):
        self.setX(fileGro)
        self.atomsTypes(fileItp)
        self.loadConstants()
        self.loadAP()
        self.determineConstants()

    def setX(self, fileName):
        with open(fileName) as f:
            input = f.readlines()

        currentLine = 1
        line = input[currentLine]

        x = []
        y = []
        z = []
        self.n = int(input[currentLine])
        self.c6 = []
        self.c12 = []

        while True:
            for i in range(0,self.n):
                currentToken = 3
                currentLine += 1
                line = input[currentLine]

                tokens = re.findall(r"[\w\.']+", line)
                x.insert(i, tokens[currentToken])
                currentToken += 1
                y.insert(i, tokens[currentToken])
                currentToken += 1
                z.insert(i, tokens[currentToken])

            currentLine += 1
            if len(input) > currentLine + 1:
                currentLine += 1
            else:
                break

            currentLine += 1

        self.m = len(x)
        self.X = [[0 for self.X in xrange(3)] for self.X in xrange(self.m)]

        for i in xrange(0,self.m):
            self.X[i][0] = float(x[i]) * 10
            self.X[i][1] = float(y[i]) * 10
            self.X[i][2] = float(z[i]) * 10

    def atomsTypes(self, fileName):
        with open(fileName) as f:
            input = f.readlines()

        self.types = []
        self.cargos = []

        currentLine = 0
        line = input[currentLine]

        tokens = re.findall(r"[\w\.']+", line)
        token = ""
        
        while token != "atoms":
            currentToken = 0
            currentLine += 1
            line = input[currentLine]

            if line != "":
                tokens = re.findall(r"[\w\.\-\+\[\]\;\n\=']+", line)

                if tokens[currentToken] == "[":
                    currentToken += 1
                    token = tokens[currentToken]

        currentLine = currentLine + 2
        line = input[currentLine]
        for i in xrange(0,self.n):
            tokens = re.findall(r"[\w\.\-\+\[\]\;\n\=']+", line)
            currentToken = 1
            self.types.insert(i, tokens[currentToken])
            currentToken += 5
            self.cargos.insert(i, tokens[currentToken])
            currentLine += 1
            line = input[currentLine]

    def loadConstants(self):
        with open("defaultsFiles/ffcargasnb.itp") as f:
            input = f.readlines()

        ttype = []
        sigma = []
        epsilon = []
        currentLine = 1
        line = input[currentLine]
        index = 1

        while len(input) > currentLine +1:
            currentToken = 0
            currentLine += 1
            line = input[currentLine]
            tokens = re.findall(r"[\w\.\-\+']+", line)
            ttype.insert(index, tokens[currentToken])
            currentToken += 4
            sigma.insert(index, tokens[currentToken])
            currentToken += 1
            epsilon.insert(index, tokens[currentToken])

        nttypes = len(ttype)
        self.typeConstants = []
        self.constantc6 = []
        self.constantc12 = []

        for i in xrange(0,nttypes):
            self.typeConstants.insert(i, ttype[i])
            self.constantc6.insert(i, 4.0 * float(epsilon[i]) * (float(sigma[i]) ** 6))
            self.constantc12.insert(i, 4.0 * float(epsilon[i]) * (float(sigma[i]) ** 12))

    def loadAP(self):
        with open("defaultsFiles/AtomProva.atp") as f:
            input = f.readlines()

        self.ap = []
        self.cargosap = []
        self.c6ap = []
        self.c12ap = []

        currentLine = 1
        line = input[currentLine]
        index = 0

        while len(input) > currentLine + 1:
            currentToken = 0
            currentLine += 1
            line = input[currentLine]
            tokens = re.findall(r"[\w\.\-\+\(\)\=']+", line)
            self.ap.insert(index, tokens[currentToken])
            currentToken += 1
            self.cargosap.insert(index, float(tokens[currentToken]))
            currentToken += 1
            self.c6ap.insert(index, float(tokens[currentToken]))
            currentToken += 1
            self.c12ap.insert(index, float(tokens[currentToken]))
            index += 1

    def determineConstants(self):
        for i in xrange(0,self.n):
            index = self.search(self.typeConstants, self.types[i])
            self.c6.insert(i, self.constantc6[index])
            self.c12.insert(i, self.constantc12[index])

    def search(self, vector, element):
        nelem = len(vector)

        for i in xrange(0,nelem):
            if element == vector[i]:
                return i

        return -1
        
    def gridGenerate(self, I, J, K, atp, dx, dy, dz):
        f = 138.935485
        nframes = self.m / self.n
        natp = len(atp)
        self.gridCoulomb = [[[[0 for x in xrange(natp)] for x in xrange(K)] for x in xrange(J)] for x in xrange(I)]
        self.gridLJ = [[[[0 for x in xrange(natp)] for x in xrange(K)] for x in xrange(J)] for x in xrange(I)]

        for h in xrange(0, natp):
            elem = self.search(self.ap, atp[h])
            q1 = self.cargosap[elem]
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
                        npontos += 1

                        for l in xrange(0,self.m):
                            r = self.distance(r1, self.X[l]) / 10
                            index = l % self.n
                            c6ij = math.sqrt(c6a * self.c6[index])
                            c12ij = math.sqrt(c12a * self.c12[index])
                            Vlj = Vlj + (c12ij / (math.pow(r, 12))) - (c6ij / (math.pow(r, 6)))
                            Vc = Vc + f * float(q1) * float(self.cargos[index]) / r

                        self.gridCoulomb[i][j][k][h] = Vc / nframes
                        self.gridLJ[i][j][k][h] = Vlj / math.sqrt(nframes)

    def distance(self, r1, r2):
        d = math.sqrt(math.pow((r1[0] - r2[0]), 2) + math.pow((r1[1] - r2[1]) ,2) + math.pow((r1[2] - r2[2]), 2))
        return d

    def saveGrids(self):
        output = ""
        coulomb = ""
        lj = ""

        I = len(self.gridCoulomb)
        J = len(self.gridCoulomb[0])
        K = len(self.gridCoulomb[0][0])
        L = len(self.gridCoulomb[0][0][0])
        
        for i in xrange(0,I):
            for j in xrange(0,J):
                for k in xrange(0,K):
                    for l in xrange(0,L):
                        pass
                        coulomb = "%f\t" % (self.gridCoulomb[i][j][k][l])
                        lj = "%f\t" % (self.gridLJ[i][j][k][l])
        
        output = coulomb + "\n" + lj
        return output
