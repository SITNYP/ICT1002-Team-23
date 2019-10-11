import pandas as pd
import matplotlib.pyplot as plt
#import numpy as np
from PyQt4.QtGui import QFileDialog, QTableWidget, QTableWidgetItem, QSortFilterProxyModel, QMessageBox

def fileUpload(filePath): #takes in the file path and returns it as a pandas csv variable
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

# takes in 4 variables, dataset (integrate with file), x axis to plot (int - col number),
# y axis to plot (int - col number), the groups to plot by (set to none by default, if no groupby is selected, the arguement is null)


def plot(data, graphType, x, y, desiredPlots=None):
    if desiredPlots != "None":
        #groups the specified column
        fig, ax = plt.subplots()
        groupedData = data.groupby(data.columns[desiredPlots])
        for key, item in groupedData:
            groups = groupedData.get_group(key)
            #plots the graph
            groups.plot(kind=graphType, x=data.columns[x], y=data.columns[y], ax=ax, label=key, figsize=(16, 6))
            #sets labels
            plt.xlabel(data.columns[x])
            plt.ylabel(data.columns[y])
            #plt.title("add file name here")
        #plt.show()
        return ax
    else:
        #plots the graph
        graph = data.plot(kind=graphType, x=data.columns[x], y=data.columns[y], figsize=(16, 6))
        #sets labels
        plt.xlabel(data.columns[x])
        plt.ylabel(data.columns[y])
        #plt.title("add file name here")
        #plt.show()
        return graph

#main problem is that when there are multiple groups, it will not take the dataset well. E.g. multiple groupby we can do