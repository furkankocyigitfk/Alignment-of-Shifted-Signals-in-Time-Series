import numpy as np
import math
import copy
import csv
import matplotlib.pyplot as plt


# warpedSegments 0-->source index,1-->destination index,2-->distance
# lines[i][0]-->x's values
# lines[i][1]-->y's values

class COWFunctions():
    def __init__(self, signal1, segmentLength, slack):
        self.segmentLength = segmentLength
        self.slack = slack
        self.signal1 = copy.copy(signal1)
        self.signal2 = None

    def updateSignal2(self, signal2):
        self.signal2 = copy.copy(signal2)

    def calculateBenefit(self, x, u, i):
        nth = self.segmentLength + u + 1
        mid1 = 0
        mid2 = 0
        mid1x1 = 0
        mid2x2 = 0
        mid1x2 = 0
        mid1 = np.float64(mid1)
        mid2 = np.float64(mid2)
        mid1x1 = np.float64(mid1x1)
        mid2x2 = np.float64(mid2x2)
        mid1x2 = np.float64(mid1x2)

        for j in range(self.segmentLength + u + 1):
            popr = j * self.segmentLength / (self.segmentLength + u)
            if math.floor(popr) < 0:
                popr = 0
            if math.ceil(popr) > self.segmentLength:
                popr = self.segmentLength

            frak = popr - math.floor(popr)
            pl = int(i * self.segmentLength + math.floor(popr))
            ph = int(i * self.segmentLength + math.ceil(popr))

            m1 = self.signal1[x + j]
            m2 = (1 - frak) * self.signal2[pl] + frak * self.signal1[ph]

            mid1 += m1
            mid2 += m2
            mid1x1 += m1 ** 2
            mid2x2 += m2 ** 2
            mid1x2 += m1 * m2

        result = (mid1x2 - (mid1 * mid2) / nth) / math.sqrt((mid1x1 - mid1 ** 2 / nth) * (mid2x2 - mid2 ** 2 / nth))
        return result

    def getAlignedSignals(self, warpedSegments):
        # warpedSegments 0-->source index,1-->destination index,2-->distance
        result = [0.0 for i in range(len(self.signal2))]
        for i in range(len(warpedSegments) - 1):
            wDiff = warpedSegments[i + 1][0] - warpedSegments[i][0]
            xDiff = warpedSegments[i + 1][1] - warpedSegments[i][1]
            for j in range(wDiff + 1):
                lEx = warpedSegments[i][1] + j * xDiff / wDiff
                frak = lEx - math.floor(lEx)
                pl = int(math.floor(lEx))
                ph = int(math.ceil(lEx))

                if pl < 0:
                    pl = 0
                if ph > len(self.signal2):
                    ph = len(self.signal2)
                result[warpedSegments[i][0] + j] = (1 - frak) * self.signal2[pl] + frak * self.signal2[ph]
        return result

    def getWarpedSegments(self):
        n1 = len(self.signal1)
        n2 = len(self.signal2)
        F = [-np.inf for _ in range(n1 * 2)]
        F[n1 - 1] = 0
        temp = 1 if n2 % self.segmentLength == 0 else 0
        n = n2 // self.segmentLength - temp
        delta = n1 // n - self.segmentLength
        uOptX = np.zeros(n1 * n, dtype="int")
        uOpt = np.zeros(n, dtype="int")
        xOpt = np.zeros(n + 1, dtype="int")

        for i in range(n - 1, -1, -1):
            for x in range(n1):
                F[n1 + x] = F[x]
                F[x] = -np.inf

            xStart = i * (self.segmentLength + delta - self.slack)
            if (xStart < n1 - 1 - (n - i) * (self.segmentLength + delta + self.slack)):
                xStart = n1 - 1 - (n - i) * (self.segmentLength + delta + self.slack)

            xEnd = i * (self.segmentLength + delta + self.slack)
            if (xEnd > n1 - 1 - (n - i) * (self.segmentLength + delta - self.slack)):
                xEnd = n1 - 1 - (n - i) * (self.segmentLength + delta - self.slack)

            for x in range(xStart, xEnd + 1):
                for u in range(delta - self.slack, delta + self.slack + 1):
                    if 0 <= x + self.segmentLength + u < n1 and F[n1 + x + self.segmentLength + u] > -n:
                        fsum = F[n1 + x + self.segmentLength + u] + self.calculateBenefit(x, u, i)
                        if fsum > F[x]:
                            F[x] = fsum
                            uOptX[i * n1 + x] = u

        xOpt[0] = 0
        for i in range(n):
            uOpt[i] = uOptX[i * n1 + xOpt[i]]
            xOpt[i + 1] = xOpt[i] + self.segmentLength + uOpt[i]

        result = list()
        for i in range(len(xOpt)):
            j = xOpt[i]
            k = i * self.segmentLength
            if (i == len(xOpt) - 1):
                k = j
            y = (self.signal1[j] - self.signal2[k]) ** 2 + (j - k) ** 2
            result.append([j, k, math.sqrt(y)])

        return result

    def forPlotWarpedSegments(self, warpedSegments):
        signal1Peaks = [warpedSegments[i][0] for i in range(len(warpedSegments))]
        signal2Peaks = [warpedSegments[i][1] for i in range(len(warpedSegments))]
        lines = list()
        for i in range(len(warpedSegments)):
            line = [[signal1Peaks[i], signal2Peaks[i]], [self.signal1[signal1Peaks[i]], self.signal2[signal2Peaks[i]]]]
            lines.append(line)

        return lines


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
    ca = COWFunctions(10, 3)
    warpedSegments = ca.getWarpedSegments(data[0], data[1])
    ca.forPlotWarpedSegments(data[0], data[1], warpedSegments)
    # warpedSegments[0], warpedSegments[1] = warpedSegments[1], warpedSegments[0]
    """alignedSignal = ca.getAlignedSignals(data[0], data[1], warpedSegments)
    plt.plot(data[0], color="red")
    plt.plot(alignedSignal[1], color="blue")
    plt.plot(data[1], color="green")
    plt.show()"""
