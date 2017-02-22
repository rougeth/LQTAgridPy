#!/usr/bin/env
# coding: utf-8

import matrix_generate
#from . import matrix_generate, utils
import utils
from numpy import arange
import os
from pandas import DataFrame


class GridGenerate():

    def __init__(self, coordinates, dimensions, atp, directory, step):

        #dataFile = open(files).read().splitlines()
        dataFile = os.listdir(directory)
        self.molecules = [x.replace('.gro','') for x in dataFile if x.endswith('gro')]
        self.molecules.sort()
        dataFile = [directory+'/'+fileName for fileName in dataFile]
        groFiles = [x for x in dataFile if x.endswith('gro')]
        groFiles.sort()
        # topFiles = [x for x in dataFile if x.endswith('top')]
        # topFiles.sort()
        topFiles = []
        for x in groFiles:
            topFiles.append(x[:-8]+'.top')
        itpFiles = [x for x in dataFile if x.endswith('nb.itp')]
        itpFiles.sort()
        # print([arq.split('/')[-1] for arq in topFiles])
        # print([arq.split('/')[-1] for arq in groFiles])
        # print([arq.split('/')[-1] for arq in itpFiles])
        matrices = []

        minimos = [999999.0,999999.0,999999.0]
        maximos = [-999999.0,-999999.0,-999999.0]
        #for fileGro, fileItp, fileTop in utils.pairwise(dataFile):
        #for fileGro, fileTop, fileItp in utils.triplewise(dataFile):
        for i in range(len(groFiles)):
            matrix = matrix_generate.MatrixGenerate(groFiles[i], topFiles[i], itpFiles[i])
            minimos[0] = min(minimos[0],matrix.minimos[0])
            minimos[1] = min(minimos[1],matrix.minimos[1])
            minimos[2] = min(minimos[2],matrix.minimos[2])
            maximos[0] = max(maximos[0],matrix.maximos[0])
            maximos[1] = max(maximos[1],matrix.maximos[1])
            maximos[2] = max(maximos[2],matrix.maximos[2])
            matrices.append(matrix)

        if coordinates != ():
            x0, y0, z0 = coordinates
        else:
            x0 = int(minimos[0])-5
            y0 = int(minimos[1])-5
            z0 = int(minimos[2])-5

        if dimensions != ():
            dim_x, dim_y, dim_z = dimensions
        else:
            dim_x = int(maximos[0]-minimos[0])+10
            dim_y = int(maximos[1]-minimos[1])+10
            dim_z = int(maximos[2]-minimos[2])+10

        if not step == 1:
            I = int((dim_x/step)+(1/step-1))
            J = int((dim_y/step)+(1/step-1))
            K = int((dim_z/step)+(1/step-1))
        else:
            I = dim_x + 1
            J = dim_y + 1
            K = dim_z + 1

        n = len(atp)
        coulomb = ""
        lj = ""

        self.cCoulomb = []
        self.cLJ = []
        for l in range(n):
            for i in arange(x0,dim_x+x0+step,step):
                for j in arange(y0,dim_y+y0+step,step):
                    for k in arange(z0,dim_z+z0+step,step):
                        coulomb += "%.2f_%.2f_%.2f_%s_C: \t" % (i, j,
                                                                k, atp[l])

                        lj += "%.2f_%.2f_%.2f_%s_LJ: \t" % (i, j,
                                                            k, atp[l])
                        self.cCoulomb.append("%.2f_%.2f_%.2f_%s_C:" % (i, j, k, atp[l]))
                        self.cLJ.append("%.2f_%.2f_%.2f_%s_LJ:" % (i, j, k, atp[l]))
        self.output = coulomb + lj

        self.coulombMatrix = []
        self.ljMatrix = []
        for matrix in matrices:
            matrix.gridGenerate(dim_x, dim_y, dim_z, atp, x0, y0, z0, step)
            # valuesCoulomb = matrix.getMatrix("C")
            # valuesLj = matrix.getMatrix("L")
            textValuesCoulomb, textValuesLj, coulombMatrix, ljMatrix = matrix.getMatrix()
            self.output += "\n" + textValuesCoulomb + textValuesLj
            self.coulombMatrix.append(coulombMatrix)
            self.ljMatrix.append(ljMatrix)

    def saveGrid(self,output):
        arq = open(output+'.txt', "w")
        arq.write(self.output)
        arq.close()
        dfCoulomb = DataFrame(self.coulombMatrix, columns = self.cCoulomb, index = self.molecules)
        dfLj = DataFrame(self.ljMatrix, columns = self.cLJ, index = self.molecules)
        df = dfCoulomb.join(dfLj)
        df.to_csv(output+'.csv', sep =';')
