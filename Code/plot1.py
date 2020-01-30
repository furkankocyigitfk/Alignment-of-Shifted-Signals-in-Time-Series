import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5.QtWidgets import *

import csv


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=15, height=6):
        self.x = 1
        self.figure = Figure(figsize=(width, height))
        self.figure.subplots_adjust(0.05, 0.2, 0.9, 0.8)
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        self.ax = self.figure.add_subplot(111)
        self.toolbar = NavigationToolbar(self, self)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def plotNew(self, signal1, signal2=None):
        self.ax.plot(signal1)
        if signal2 is not None:
            self.x += 1
            self.ax.plot(signal2)
        self.draw()

    def plotWarpedSegments(self, signal1, signal2, lines):
        self.figure.clear()
        ax = self.figure.subplots(1, 1)
        ax.plot(signal1)
        ax.plot(signal2)
        for i in range(len(lines)):
            ax.plot(lines[i][0], lines[i][1], color="black")
        self.draw()

    def clear(self):
        self.figure.clear()
        self.draw()
