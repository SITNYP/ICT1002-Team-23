import pandas as pd
from PyQt4.QtGui import QFileDialog, QTableWidget, QTableWidgetItem, QSortFilterProxyModel, QMessageBox
import matplotlib.pyplot as plt


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


def successGUI():
    """Display succesfully downloaded file messsage"""
    success = QMessageBox()
    success.setIcon(QMessageBox.Information)
    success.setWindowTitle("Success!")
    success.setText("File Downloaded")
    success.exec_()


#Converts all values in the column to float
#NaN is ignored by matplotlib
def plotcheckx(data, x):
    try:
        data.iloc[:, x] = data.iloc[:, x].map(lambda u: pd.to_numeric(u, errors=coerce, downcast="float"))
        return data
    except Exception as e:
        errorGUI(str(e))

def plotchecky(data, y):
    try:
        data.iloc[:, y] = data.iloc[:, y].map(lambda u: pd.to_numeric(u, errors=coerce, downcast="float"))
        return data
    except Exception as e:
        errorGUI(str(e))

def plot(data, graphType, x, y, desiredPlots=None):
    if desiredPlots > 0:
        # groups the specified column
        fig, ax = plt.subplots()
        groupedData = data.groupby(data.columns[desiredPlots])
        for key, item in groupedData:
            groups = groupedData.get_group(key)
            # plots the graph
            groups.plot(kind=graphType, x=data.columns[x], y=data.columns[y], ax=ax, label=key, figsize=(16, 6))
            # sets labels
            plt.xlabel(data.columns[x])
            plt.ylabel(data.columns[y])
        plt.show()
    else:
        # plots the graph
        data.plot(kind=graphType, x=data.columns[x], y=data.columns[y], figsize=(16, 6))
        # sets labels
        plt.xlabel(data.columns[x])
        plt.ylabel(data.columns[y])
        plt.show()

