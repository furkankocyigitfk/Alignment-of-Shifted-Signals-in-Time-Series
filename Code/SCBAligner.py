from DTWFunctions import DTWFunctions
import numpy as np
import math


class SCBAligner(DTWFunctions):
    def __init__(self, signal1, gap, bandWidth, n, T):
        super().__init__(signal1, gap, n, T)
        self.bandWidth = bandWidth

    def getCostMatrix(self):
        n1 = len(self.signal1)
        n2 = len(self.signal2)
        cost_matrix = [[0.0 for j in range(n2)] for i in range(n1)]
        rx = int(n1*self.bandWidth)
        ry = int(n2*self.bandWidth)
        distance = 0.0

        for i in range(n1):
            x = i
            b = 0 if x - ry < 0 else int(x - ry) + 1
            c = n2 if x + rx > n2 else int(x + rx)
            j = b

            while b <= j < c-1:
                if self.n == 0:
                    distance = math.sqrt((self.signal1[i] - self.signal2[j]) ** 2 + (i - j) ** 2)
                elif self.n == 1:
                    distance = abs((self.signal1[i] - self.signal2[j]) + abs(i - j))
                elif self.n == 2:
                    distance = max(abs(self.signal1[i] - self.signal2[j]), abs(i - j))
                elif self.n == 3:
                    distance = (abs(self.signal1[i] - self.signal2[j]), abs(i - j)) / abs(
                        self.signal1[i] + self.signal2[j] + i + j)
                j += 1

            distance = distance * np.exp(abs(i - j) * self.T)
            cost_matrix[i][j] = distance
        return cost_matrix

    def getAccumulatedCostMatrix(self):
        n1=len(self.signal1)
        n2=len(self.signal2)
        cost_matrix = self.getCostMatrix()
        accumulate_cost_matrix = [[0.0 for j in range(len(self.signal2))] for i in range(len(self.signal1))]
        accumulate_cost_matrix[0][0] = cost_matrix[0][0]

        for i in range(1, int(len(self.signal1) * self.bandWidth)):
            accumulate_cost_matrix[i][0] = accumulate_cost_matrix[i - 1][0] + cost_matrix[i][0]

        for i in range(1, int(len(self.signal2) * self.bandWidth)):
            accumulate_cost_matrix[i][0] = accumulate_cost_matrix[0][i - 1] + cost_matrix[0][i]

        rx = 1.0
        ry = 1.0

        for i in range(n1):
            x = i
            if i < n2 // 2:
                rx += self.bandWidth
                ry += self.bandWidth
            else:
                rx -= self.bandWidth
                ry -= self.bandWidth

            b = 1 if x - ry < 1 else int(x - ry) + 1
            c = n2 if x + rx >= n2 else int(x + rx)
            j = b

            while b <= j < c:
                accumulate_cost_matrix[i][j] = min(accumulate_cost_matrix[i - 1][j],
                                                   accumulate_cost_matrix[i][j - 1],
                                                   accumulate_cost_matrix[i - 1][j - 1]) + \
                                               cost_matrix[i][j]
                j += 1

        return accumulate_cost_matrix
