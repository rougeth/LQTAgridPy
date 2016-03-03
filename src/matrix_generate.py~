#!/usr/bin/env
# coding: utf-8

import math
import re
import utils

class MatrixGenerate():

    def __init__(self, fileGro, fileTop, fileItp):
        self.setX(fileGro)
        self.atomsTypes(fileTop)
        self.loadConstants(fileItp)
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

                #tokens = re.findall(r"[\w\.']+", line)
		tokens = line.split()
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
        self.X = [[0 for self.X in range(3)] for self.X in range(self.m)]

        self.minimos = [float(x[0]) * 10,float(y[0]) * 10,float(z[0]) * 10]
        self.maximos = [float(x[0]) * 10,float(y[0]) * 10,float(z[0]) * 10]
        for i in range(self.m):
            self.X[i][0] = float(x[i]) * 10
            self.X[i][1] = float(y[i]) * 10
            self.X[i][2] = float(z[i]) * 10
            self.minimos[0] = min(self.minimos[0],self.X[i][0])
            self.minimos[1] = min(self.minimos[1],self.X[i][1])
            self.minimos[2] = min(self.minimos[2],self.X[i][2])
            self.maximos[0] = max(self.maximos[0],self.X[i][0])
            self.maximos[1] = max(self.maximos[1],self.X[i][1])
            self.maximos[2] = max(self.maximos[2],self.X[i][2])

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
        for i in range(self.numberElements):
            tokens = re.findall(r"[\w\.\-\+\[\]\;\n\=']+", line)
            currentToken = 1
            self.types.insert(i, tokens[currentToken])
            currentToken += 5
            self.cargos.insert(i, tokens[currentToken])
            currentLine += 1
            line = input[currentLine]

    def loadConstants(self,fileName):
        with open(fileName) as f:
            input = f.readlines()

        ttype = []
        sigma = []
        epsilon = []
        currentLine = 0
        line = input[currentLine]
        index = 1
        
        while line != "[ atomtypes ]\n":
            currentLine += 1
            line = input[currentLine]        
        currentLine += 1
        
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
            index += 1

        nttypes = len(ttype)
        self.typeConstants = []
        self.constantc6 = []
        self.constantc12 = []

        for i in range(nttypes):
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

        for i in range(nElem):
            if element == vector[i]:
                return i

        return -1

    def determineConstants(self):
        for i in range(self.numberElements):
            index = self.search(self.typeConstants, self.types[i])
            self.c6.insert(i, self.constantc6[index])
            self.c12.insert(i, self.constantc12[index])
        
    def gridGenerate(self, dimX, dimY, dimZ, atp, x0, y0, z0, step):
        self.DimX = dimX
        self.DimY = dimY
        self.DimZ = dimZ
        self.natp = len(atp)

        f = 138.935485
        nframes = self.m / self.numberElements
        self.gridCoulomb = [[[[0 for x in range(self.natp)] for x in range(self.DimZ)]
                            for x in range(self.DimY)] for x in range(self.DimX)]

        self.gridLJ = [[[[0 for x in range(self.natp)] for x in range(self.DimZ)]
                        for x in range(self.DimY)] for x in range(self.DimX)]

        print("Dimensions %d X %d X %d\n" % (self.DimX,self.DimY,self.DimZ))
        for h in range(self.natp):
            elem = self.search(self.ap, atp[h])
            q1 = self.cargosap[elem]
            c6a = self.c6ap[elem]
            c12a = self.c12ap[elem]
            Vlj = 0
            Vc = 0
            npontos = 0
            #r1 = []
            r1 = [0.0,0.0,0.0]
	            
	    print("Calculating %s probe\n" % atp[h])
            for i in range(self.DimX):
                r1[0] = i*step+x0
                for j in range(self.DimY):
                    r1[1] = j*step+y0
                    for k in range(self.DimZ):
                        r1[2] = k*step+z0
                        Vlj = 0
                        Vc = 0
                        npontos += 1
                        for l in range(self.m):
                            r = utils.Distance(r1, self.X[l]) / 10
                            index = l % self.numberElements
                            c6ij = math.sqrt(c6a * self.c6[index])
                            c12ij = math.sqrt(c12a * self.c12[index])

			    if r != 0:
                                Vlj = Vlj + (c12ij / (math.pow(r, 12))) - (c6ij / (math.pow(r, 6)))
                                Vc = Vc + f * float(q1) * float(self.cargos[index]) / r
			    else:
			        Vlj = float("inf")
				Vc = float("inf")

                        self.gridCoulomb[i][j][k][h] = Vc / nframes
                        self.gridLJ[i][j][k][h] = Vlj / math.sqrt(nframes)

    def getMatrix(self, optionGrid):
        result = ""
        for i in range(self.DimX):
            for j in range(self.DimY):
                for k in range(self.DimZ):
                    for l in range(self.natp):
                        if optionGrid == "C":
                            result += "%g\t" % (self.gridCoulomb[i][j][k][l])
                        elif optionGrid == 'L':
                            result += "%g\t" % (self.gridLJ[i][j][k][l])
                        else:
                            pass
        return result
