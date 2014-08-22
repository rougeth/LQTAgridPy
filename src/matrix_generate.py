#!/usr/bin/env
# coding: utf-8

import math
import re
import utils

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
        self.numberElements = int(input[currentLine])
        self.c6 = []
        self.c12 = []

        while True:
            for i in range(self.numberElements):
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

        for i in xrange(self.m):
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

        currentLine += 2
        line = input[currentLine]
        for i in xrange(self.numberElements):
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

        for i in xrange(nttypes):
            self.typeConstants.insert(i, ttype[i])

            self.constantc6.insert(i, 4.0 * float(epsilon[i])
                                    * (float(sigma[i]) ** 6))
            self.constantc12.insert(i, 4.0 * float(epsilon[i])
                                    * (float(sigma[i]) ** 12))

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

    def search(self, vector, element):
        nElem = len(vector)

        for i in xrange(nElem):
            if element == vector[i]:
                return i

        return -1

    def determineConstants(self):
        for i in xrange(self.numberElements):
            index = self.search(self.typeConstants, self.types[i])
            self.c6.insert(i, self.constantc6[index])
            self.c12.insert(i, self.constantc12[index])
        
    def gridGenerate(self, dimX, dimY, dimZ, atp, x0, y0, z0, step):
        f = 138.935485
        nframes = self.m / self.numberElements
        natp = len(atp)
        self.gridCoulomb = [[[[0 for x in xrange(natp)] for x in xrange(dimZ)]
                            for x in xrange(dimY)] for x in xrange(dimX)]

        self.gridLJ = [[[[0 for x in xrange(natp)] for x in xrange(dimZ)]
                        for x in xrange(dimY)] for x in xrange(dimX)]

        for h in xrange(natp):
            elem = self.search(self.ap, atp[h])
            q1 = self.cargosap[elem]
            c6a = self.c6ap[elem]
            c12a = self.c12ap[elem]
            Vlj = 0
            Vc = 0
            npontos = 0
            r1 = []

            for i in xrange(dimX):
                r1.insert(0, i*step+x0)
                for j in xrange(dimY):
                    r1.insert(1, j*step+y0)
                    for k in xrange(dimZ):
                        r1.insert(2, k*step+z0)
                        npontos += 1
                        for l in xrange(self.m):
                            r = utils.Distance(r1, self.X[l]) / 10
                            index = l % self.numberElements
                            c6ij = math.sqrt(c6a * self.c6[index])
                            c12ij = math.sqrt(c12a * self.c12[index])

                            Vlj = Vlj + (c12ij / (math.pow(r, 12))) - (c6ij / (math.pow(r, 6)))
                            Vc = Vc + f * float(q1) * float(self.cargos[index]) / r

                        self.gridCoulomb[i][j][k][h] = Vc / nframes
                        self.gridLJ[i][j][k][h] = Vlj / math.sqrt(nframes)

    def returnGridValuePosition(self, I, J, K, L, optionGrid):
        if optionGrid == "C":
            coulomb = "%f\t" % (self.gridCoulomb[I][J][K][L])
            return coulomb
        elif optionGrid == 'L':
            lj = "%f\t" % (self.gridLJ[I][J][K][L])
            return lj
        else:
            return "Invalid Option Grid"
