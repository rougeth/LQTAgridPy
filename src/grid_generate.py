#!/usr/bin/env
# coding: utf-8

import matrix_generate
import utils

class GridGenerate():

    def __init__(self, coordinates, dimensions, atp, files, step):
        
        dataFile = open(files).read().splitlines()
        matrices = [] 

        minimos = [999999.0,999999.0,999999.0]
        maximos = [-999999.0,-999999.0,-999999.0]
        #for fileGro, fileItp, fileTop in utils.pairwise(dataFile):
        for fileGro, fileTop, fileItp in utils.triplewise(dataFile):
            matrix = matrix_generate.MatrixGenerate(fileGro, fileTop, fileItp)
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

        for i in range(I):
            for j in range(J):
                for k in range(K):
                    for l in range(n):
                        value_x = i*step+x0
                        value_y = j*step+y0
                        value_z = k*step+z0
                        coulomb += "%.2f_%.2f_%.2f_%s_C: \t" % (value_x, value_y,
                                                                value_z, atp[l])

                        lj += "%.2f_%.2f_%.2f_%s_LJ: \t" % (value_x, value_y,
                                                            value_z, atp[l])
        self.output = coulomb + lj
        
        for matrix in matrices:
            matrix.gridGenerate(I, J, K, atp, x0, y0, z0, step)
            valuesCoulomb = matrix.getMatrix("C")
            valuesLj = matrix.getMatrix("L")
            self.output += "\n" + valuesCoulomb + valuesLj            
            
    def saveGrid(self,output):
        arq = open(output, "w")
        arq.write(self.output)
        arq.close()
        