import math

class matrixGenerate():

    def __init__(self, fileGro, fileItp):
        setX(fileGro)
        atomsTypes(fileItp)
        loadConstants()
        loadAP()
        determineConstants()

    def setX(fileName):
        with open(fileName) as f:
            input = f.readlines()

        currentLine = 1
        line = input[currentLine]
        line = input[currentLine]

        x = []
        y = []
        z = []
        # self.n = input.nextInt();
        self.types = []
        self.cargos = []
        self.c6 = []
        self.c12 = []

        currentToken = 3

        while True:
            for i in xrange(0,self.n):
                line = input[++currentLine]
                
                tokens = line.split(' ')
                x.insert(i, tokens[++currentToken])
                y.insert(i, tokens[++currentToken])
                z.insert(i, tokens[++currentToken])

            ++currentLine
            if input[currentLine + 1] != None:
                ++currentLine
            else
                break;

            ++currentLine 

        self.m = len(x)
        self.X = [[0 for x in xrange(m)] for x in xrange(3)]

        for i in xrange(0,self.m):
            self.X[i][0] = (x.[i]) * 10
            self.X[i][1] = (y.[i]) * 10
            self.X[i][2] = (z.[i]) * 10

    def atomsTypes(fileName):
        with open(fileName) as f:
            input = f.readlines()

        currentLine = 22
        currentToken = 2
        line = input[currentLine]

        tokens = line.split(' ')
        token = tokens[currentToken]
        
        while token != "atoms":
            line = input[++currentLine]

            if line != "":
                tokens = line.split(' ')

                if tokens[currentToken] == "[":
                    token = tokens[++currentToken]

        currentLine = currentLine + 2
        line = input[currentLine]

        for i in xrange(0,self.n):
            tokens = line.split(' ')
            currentToken = 3
            self.types[i] = tokens[currentToken]

            for j in xrange(0,4):
                ++currentToken
                self.cargos[i] = tokens[++currentToken]
                line = input[++currentLine]



    def loadConstants():
        with open(fileName) as f:
            input = f.readlines()

        ttype = []
        sigma = []
        epsilon = []
        currentLine = 2
        currentToken = 1
        line = input[currentLine]
        index = 1

        while input[currentLine+1] != None:
            line = input[++currentLine]
            tokens = line.split(' ')
            ttype.insert(index, tokens[++currentToken])
            currentToken = currentToken +3
            sigma.insert(index, tokens[++currentToken]);
            epsilon.insert(index, tokens[++currentToken]);
            ++index

        nttypes = len(ttype)
        self.typeConstants = []
        self.constantc6 = []
        self.constantc12 = []

        for i in xrange(0,nttypes):
            self.typeConstants.insert(i, ttype[i])
            self.constantc6.insert(i, 4 * epsilon[i] * math.pow(sigma[i], 6))
            self.constantc12.insert(i, 4 * epsilon[i] * math.pow(sigma[i], 12))

    def loadAP():
        with open("AtomProva.atp") as f:
            input = f.readlines()

        self.ap = []

        currentLine = 3
        currentToken = 1
        line = input[currentLine]

        while input[currentLine+1] != None:
            index = 0
            line = input[++currentLine]
            tokens = line.split(' ')
            self.ap[index] = tokens[++currentToken]
            self.cargosap[index] = tokens[++currentToken]
            self.c6ap[index] = tokens[++currentToken]
            self.c12ap[index] = tokens[++currentToken]
            ++index

    def determineConstants():
        for i in xrange(0,self.n):
            index = search(self.typeConstants, self.types[i])
            self.c6[i] = self.constantc6[index]
            self.c12[i] = self.constantc12[index]

    def search(vector, element):
        nelem = len(vector)

        for i in xrange(0,nelem):
            if element == vector[i]:
                return i

        return -1

    def distance(r1, r2):
        d = math.sqrt(math.pow((r1[0] - r2[0]), 2) + math.pow((r1[1] - r2[1]) ,2) + math.pow((r1[2] - r2[2]), 2))
        return d
        
    def gridGenerate(I, J, K, atp, dx, dy, dz):
        f = 138.935485
        nframes = self.m / self.n
        natp = len(atp)
        self.gridCoulomb = [[[[0 for x in xrange(I)] for x in xrange(J)] for x in xrange(K)] for x in xrange(natp)]
        self.gridLJ = [[[[0 for x in xrange(I)] for x in xrange(J)] for x in xrange(K)] for x in xrange(natp)]

        for h in xrange(0, natp):
            elem = search(self.ap, atp[h])
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
    