import numpy as np
import copy
import math
import csv
import matplotlib.pyplot as plt


class DTWFunctions():
    def __init__(self, signal1, gap, n, T):
        self.gap = gap
        self.signal1 = copy.copy(signal1)
        self.signal2 = None
        self.n = n
        self.T = T

    def updateSignal2(self, signal2):
        self.signal2 = copy.copy(signal2)

    def getCostMatrix(self):

        n1 = len(self.signal1)
        n2 = len(self.signal2)
        cost_matrix = [[0.0 for j in range(n2)] for i in range(n1)]

        for i in range(n1):
            for j in range(n2):
                if self.n == 0:
                    distance = math.sqrt((self.signal1[i] - self.signal2[j]) ** 2 + (i - j) ** 2)
                elif self.n == 1:
                    distance = abs((self.signal1[i] - self.signal2[j]) + abs(i - j))
                elif self.n == 2:
                    distance = max(abs(self.signal1[i] - self.signal2[j]), abs(i - j))
                elif self.n == 3:
                    distance = (abs(self.signal1[i] - self.signal2[j]), abs(i - j)) / abs(
                        self.signal1[i] + self.signal2[j] + i + j)

                distance = distance * np.exp(abs(i - j) * self.T)
                cost_matrix[i][j] = distance

        return cost_matrix

    def getAccumulatedCostMatrix(self):
        cost_matrix = self.getCostMatrix()

        accumulate_cost_matrix = [[0.0 for j in range(len(self.signal2))] for i in range(len(self.signal1))]
        accumulate_cost_matrix[0][0] = cost_matrix[0][0]

        for i in range(1, len(self.signal1)):
            accumulate_cost_matrix[i][0] = accumulate_cost_matrix[i - 1][0] + cost_matrix[i][0]
            accumulate_cost_matrix[i][0] = accumulate_cost_matrix[0][i - 1] + cost_matrix[0][i]

        for i in range(1, len(self.signal1)):
            for j in range(1, len(self.signal2)):
                accumulate_cost_matrix[i][j] = min(accumulate_cost_matrix[i - 1][j],
                                                   accumulate_cost_matrix[i][j - 1],
                                                   accumulate_cost_matrix[i - 1][j - 1]) + \
                                               cost_matrix[i][j]
        return accumulate_cost_matrix

    def getWarpedPath(self):
        accumulate_cost_matrix = self.getAccumulatedCostMatrix()

        warping_path = list()
        a = len(self.signal1) - 1
        b = len(self.signal2) - 1

        warping_path.append([a, b, accumulate_cost_matrix[a][b]])

        xMax = 0
        yMax = 0
        while (a > 0 or b > 0):

            if a == 0:
                b -= 1
            elif b == 0:
                a -= 1
            else:
                x = accumulate_cost_matrix[a - 1][b]
                y = accumulate_cost_matrix[a][b - 1]
                z = accumulate_cost_matrix[a - 1][b - 1]
                dizi = [0] * 3
                dizi[0] = min(x, y, z)
                dizi[2] = max(x, y, z)
                if dizi[0] != x and dizi[2] != x:
                    dizi[1] = x
                elif dizi[0] != y and dizi[2] != y:
                    dizi[1] = y
                else:
                    dizi[1] = z

                for element in dizi:
                    if element == x and a > 0 and xMax < self.gap:
                        a -= 1
                        xMax += 1
                        yMax = 0
                        break
                    elif element == y and b > 0 and yMax < self.gap:
                        b -= 1
                        yMax += 1
                        xMax = 0
                        break
                    elif element == z:
                        a -= 1
                        b -= 1
                        xMax = 0
                        yMax = 0
                        break

            warping_path.append([a, b, accumulate_cost_matrix[a][b]])
        return warping_path

    def getAlignedSignal(self, warping_path):
        aligned_signal = [0] * len(self.signal2)
        count = [0] * len(self.signal1)
        for elements in warping_path:
            count[elements[0]] += 1
            aligned_signal[elements[0]] += self.signal2[elements[1]]

        for i in range(len(count)):
            aligned_signal[i] /= count[i]

        return aligned_signal

    def forPlotWarpedSegments(self, warping_path):
        signal1Peaks = [warping_path[i][0] for i in range(len(warping_path))]
        signal2Peaks = [warping_path[i][1] for i in range(len(warping_path))]
        lines = list()
        for i in range(len(warping_path)):
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

    dtw = DTWFunctions(data[0], 2, 0, 0)
    dtw.updateSignal2(data[1])

    plt.plot(data[1])
    warping_path=dtw.getWarpedPath()
    lines = dtw.forPlotWarpedSegments(warping_path)
    for i in range(len(lines)):
        plt.plot(lines[i][0], lines[i][1], color="black")
    plt.plot(data[0])
    """dtw.getAlignedSignal()
    plt.plot(dtw.aligned_signal)"""
    plt.show()
    # warpedSegments[0], warpedSegments[1] = warpedSegments[1], warpedSegments[0]
    """alignedSignal = ca.getAlignedSignals(data[0], data[1], warpedSegments)
    plt.plot(data[0], color="red")
    plt.plot(alignedSignal[1], color="blue")
    plt.plot(data[1], color="green")
    plt.show()"""
