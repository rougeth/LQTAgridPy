#!/usr/bin/env
# coding: utf-8

import matrix_generate
import utils

class GridGenerate():

    def __init__(self, x0, y0, z0, dim_x, dim_y, dim_z, atp, files, step):
        coulomb = ""
        lj = ""

        if not step == 1: 
            I = int((dim_x/step)+(1/step-1))
            J = int((dim_y/step)+(1/step-1))
            K = int((dim_z/step)+(1/step-1))
        else:
            I = dim_x + 1
            J = dim_y + 1
            K = dim_z + 1

        n = len(atp)

        for i in xrange(I):
            for j in xrange(J):
                for k in xrange(K):
                    for l in xrange(n):
                        value_x = i*step+x0
                        value_y = j*step+y0
                        value_z = k*step+z0
                        coulomb += "%.2f_%.2f_%.2f_%s_C: \t" % (value_x, value_y,
                                                                value_z, atp[l])

                        lj += "%.2f_%.2f_%.2f_%s_LJ: \t" % (value_x, value_y,
                                                            value_z, atp[l])
        self.output = coulomb + lj

        dataFile = open(files).read().splitlines() 

        for fileGro, fileItp in utils.pairwise(dataFile):
            matrix = matrix_generate.MatrixGenerate(fileGro, fileItp)
            matrix.gridGenerate(I, J, K, atp, x0, y0, z0, step)
            valuesCoulomb = matrix.getMatrix("C")
            valuesLj = matrix.getMatrix("L")
            self.output += "\n" + valuesCoulomb + valuesLj

    def saveGrid(self):
        arq = open("test.txt", "w")
        arq.write(self.output)
        arq.close()
        