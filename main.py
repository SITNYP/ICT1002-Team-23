from PyQt4 import QtCore, QtGui, uic
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import modules as mod
import sys


def importCSV(self):
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Main.ui', self)
        self.show()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())