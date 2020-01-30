import numpy as np
import copy
import math
import csv
import matplotlib.pyplot as plt


# quadWarp 0-->warpingFunc,1-->pointsOfT,2-->coefficient
# interpolatedSignal 0-->signal,1-->pointsOfT,2-->gradients

class PTWFunctions():
    def __init__(self, signal1, isSmooth, delta, gap, warpingFunctions):
        self.delta = delta
        self.warpingFunctions = warpingFunctions
        self.signal1 = copy.copy(signal1)
        self.isSmooth = isSmooth
        self.gap = gap
        self.signal2 = None

    def updateSignal2(self, signal2):
        self.signal2 = copy.copy(signal2)

    def getWarpedSignals(self):
        if (self.isSmooth):
            self.signal1 = self.smoothSignal(self.signal1, 2)
            self.signal2 = self.smoothSignal(self.signal2, 2)
        qwm = self.quadWarp()
        pointsOfT = qwm[1]
        interpolatedSignal = self.interpolateSignal(qwm[0])[0]
        warpedSignal = copy.copy(self.signal2)
        for i in range(self.gap):
            warpedSignal[pointsOfT[i]] = interpolatedSignal[i]
        for i in range(self.gap - 1, len(pointsOfT)-1):
            dist = 0
            for j in range(self.gap - 1):
                dist += pointsOfT[i - j] - pointsOfT[i - j - 1]
            if dist == 0:
                pointsOfT[i] += 1
                print("kaydırma ok")
            warpedSignal[pointsOfT[i]] = interpolatedSignal[i]
        return warpedSignal

    def quadWarp(self):
        # assignments
        n1 = len(self.signal1)
        n2 = len(self.signal2)

        m = n2 if n2 > n1 else n1
        b = np.zeros((m, 3), dtype="double")
        for i in range(m):
            b[i][0] = 1
            b[i][1] = i + 1
            b[i][2] = ((i + 1) / m) ** 2

        coefficient = np.array(self.warpingFunctions, dtype="double")
        rmsOld = 0.0
        for j in range(40):
            wFunction = b.dot(np.asmatrix(coefficient).transpose())
            wFunction = np.ravel(wFunction, order='F')

            pim = self.interpolateSignal(wFunction)
            interpolatedSignal = pim[0]  # np array olarak düsün
            pointsOfT = pim[1]
            gradients = pim[2]

            residuals = np.zeros(len(pointsOfT), dtype="double")
            rms = 0

            for i in range(len(residuals)):
                residuals[i] = self.signal1[pointsOfT[i]] - interpolatedSignal[i]
                rms += residuals[i] ** 2

            rms = math.sqrt(rms / m)
            rmsDiff = abs((rms - rmsOld) / (rms + 1e-10))

            if (rmsDiff < 1e-6):
                break

            rmsOld = rms

            # gradients i matris yap sonra matrisi kopylayarak buyut
            g = np.tile(np.asmatrix(gradients).transpose(), (1, 3))

            tmp = [b[pointsOfT[i]] for i in range(len(pointsOfT))]
            tmp = np.asmatrix(tmp)
            q = np.multiply(g, tmp)

            tmp = q.I  # q nun tersi
            tmp1 = np.asmatrix(residuals, dtype="double").transpose()  # residual matris yapma
            da = tmp.dot(tmp1)  # q nun tersi * residual

            tmp = np.asmatrix(coefficient).transpose()
            coefficient = tmp + da
            coefficient = np.ravel(coefficient, order='F')

        coefficient[2] /= m ** 2

        return wFunction, pointsOfT, coefficient

    def interpolateSignal(self, warpingFunction):
        interpolatedSignal = list()
        gradients = list()
        pointsOfT = list()
        n = len(self.signal2)

        for i in range(len(warpingFunction)):
            coefficient = warpingFunction[i]
            if 1 < coefficient < n:
                floor = int(math.floor(coefficient))
                fraction = coefficient - floor
                gradient = self.signal2[floor] - self.signal2[floor - 1]

                pointsOfT.append(i)
                interpolatedSignal.append(self.signal2[floor - 1] + fraction * gradient)
                gradients.append(gradient)

        return interpolatedSignal, pointsOfT, gradients

    def smoothSignal(self, signal, diffPenalty):
        speye = np.identity(len(signal))
        diff = np.identity(len(signal))
        for i in range(diffPenalty):
            diff = diff[1:len(diff)][:] - diff[:len(diff) - 1][:]

        tmp = speye + (diff.T.dot(diff)) * self.delta
        cd = np.asmatrix(np.linalg.cholesky(tmp))
        chol = cd.T
        signalToMatrix = np.asmatrix(np.array(signal, dtype="double")).transpose()
        tmp = chol.I.dot(cd.I.dot(signalToMatrix))
        tmp = np.ravel(tmp, order='F')
        return tmp


if __name__ == "__main__":
    file = open(r"C:\Users\Furkan Koçyiğit\Desktop\data.txt", "r")
    tsvData = csv.reader(file, delimiter="\t")
    ncol = len(next(tsvData))
    data = [None] * ncol
    file.seek(0)
    for i in range(ncol):
        data[i] = list()

    for row in tsvData:
        for i in range(ncol):
            data[i].append(int(row[i]))
    file.close()
    ptw = PTWFunctions(1e5, (0, 1, 0))
    plt.plot(data[0], color="red")
    plt.plot(data[1], color="green")
    plt.plot(ptw.getWarpedSignals(data[0], data[1], False)[1], color="blue")
    plt.show()
