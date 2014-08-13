import matrix_generate

class GridGenerate():

    def __init__(self, x0, y0, z0, dim_x, dim_dy, dim_dz, atp, fileGro, fileItp, step):
        coulomb = ""
        lj = ""

        I = int((dim_x/step)-(1/step-1))
        J = int((dim_dy/step)-(1/step-1))
        K = int((dim_dz/step)-(1/step-1))
        n = len(atp)

        for i in xrange(I):
            for j in xrange(J):
                for k in xrange(K):
                    for l in xrange(n):
                        value_x = i*step+x0
                        value_y = j*step+y0
                        value_z = k*step+z0
                        coulomb += "%.2f_%.2f_%.2f_%s_C \t" % (value_x, value_y,
                                                                value_z, atp[l])
                        lj += "%.2f_%.2f_%.2f_%s_LJ \t" % (value_x, value_y,
                                                            value_z, atp[l])

        self.output = coulomb + lj + "\n"
        GMC = matrix_generate.MatrixGenerate(fileGro, fileItp)
        GMC.gridGenerate(I,J,K,atp,x0,y0,z0)
        self.output += "\n" + GMC.saveGrids() + "\n"

    def saveGrid(self):
        arq = open("test.txt", "w")
        arq.write(self.output)
        arq.close()
        