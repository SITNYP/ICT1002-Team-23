import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PyQt4.QtGui import QFileDialog, QTableWidget, QTableWidgetItem, QSortFilterProxyModel

def fileUpload(filePath): #takes in the file path and returns it as a pandas csv variable
    #if filePath.lower().endswith('.csv'):
    data = pd.read_csv(filePath)
    return data

def openFileLocation(self):
    options = QFileDialog.Options()
    fileName = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)", options=options)
    return str(fileName)