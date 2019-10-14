import pandas as pd
import matplotlib.pyplot as plt
# import numpy as np
from PyQt4.QtGui import QFileDialog, QTableWidget, QTableWidgetItem, QSortFilterProxyModel, QMessageBox


def fileUpload(filePath):  # takes in the file path and returns it as a pandas csv variable
    """Uploads the user's file and returns a Pandas CSV variable"""
    if filePath.lower().endswith('.csv'):
        data = pd.read_csv(filePath)
        return data
    else:
        raise ValueError("Please upload a CSV File!")


def openFileLocation(self):
    """Prompts user to upload a file"""
    options = QFileDialog.Options()
    fileName = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)", options=options)
    return str(fileName)


def saveFileLocation(self):
    """Prompts user where to save the file"""
    options = QFileDialog.Options()
    fileName = QFileDialog.getSaveFileName(self, "Save as", "", "CSV(*.csv)", options=options)
    return str(fileName)


def errorGUI(error):
    # Display error messsage
    warning = QMessageBox()
    warning.setIcon(QMessageBox.Critical)
    warning.setWindowTitle("Error!")
    warning.setText(error)
    warning.exec_()

# takes in 5 variables, dataset (integrate with file), x axis to plot (int - col number),
# y axis to plot (int - col number), the groups to plot by (set to none by default,
# if no groupby is selected, the argument is null)
def plot(data, graphType, x, y, desiredPlots=None):
    if desiredPlots > 0:
        fig, ax = plt.subplots()
        groupedData = data.groupby(data.columns[desiredPlots])
        for key, item in groupedData:
            groups = groupedData.get_group(key)
            groups.plot(kind=graphType, x=data.columns[x], y=data.columns[y], ax=ax, label=key,
                        figsize=(16, 6))
            plt.xlabel(data.columns[x])
            plt.ylabel(data.columns[y])
        return ax
    elif desiredPlots is None:
        fig, ax = plt.subplots()
        data.plot(kind=graphType, x=data.columns[x], y=data.columns[y], figsize=(16, 6))
        plt.xlabel(data.columns[x])
        plt.ylabel(data.columns[y])
        return ax
