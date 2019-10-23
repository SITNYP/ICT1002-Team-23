import itertools
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import pandas as pd
from PyQt4.QtGui import QFileDialog, QMessageBox
import sklearn
from sklearn import linear_model
from sklearn import metrics
import numpy as np

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


# Converts all values in the columns to floats (NaN is a float)
def convertfloatX(data, x):
    try:
        data.iloc[:, x] = data.iloc[:, x].map(lambda u: pd.to_numeric(u, errors=coerce, downcast="float"))
        return data
    except Exception as e:
        errorGUI(str(e))


def convertfloatY(data, y):
    try:
        data.iloc[:, y] = data.iloc[:, y].map(lambda u: pd.to_numeric(u, errors=coerce, downcast="float"))
        return data
    except Exception as e:
        errorGUI(str(e))

def defineplot(x):
    if x == "None":
        return None
    else:
        a = int(x[0])
        return a

def plot(data, graphType, x, y, desiredPlots=None):
    if desiredPlots > 0:
        # groups the specified column
        fig, ax = plt.subplots()
        groupedData = data.groupby(data.columns[desiredPlots])
        colors = itertools.cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        for key, item in groupedData:
            groups = groupedData.get_group(key)
            # checks that the number of groups do not exceed 20
            if len(groupedData.groups.keys()) > 20:
                raise ValueError("Too many values to be grouped, your graph could not be generated "
                                 "or could not be generated accurately")
            try:
                int(data.iloc[1,y])
                int(data,iloc[1,x])
            except Exception:
                raise TypeError("Strings cannot be used to plot a graph")
            else:
                pass
            # plots the graph
            groups.plot(kind=graphType, x=data.columns[x], y=data.columns[y], ax=ax, label=key, figsize=(16, 6),
                        color=next(colors))
            # sets labels
            plt.xlabel(data.columns[x])
            plt.ylabel(data.columns[y])
            plt.title(data.columns[x] + " vs " + data.columns[y])
        plt.show()
    else:
        # plots the graph
        data.plot(kind=graphType, x=data.columns[x], y=data.columns[y], figsize=(16, 6))
        # sets labels
        plt.xlabel(data.columns[x])
        plt.ylabel(data.columns[y])
        plt.show()

def plot_lr(data, x, y, z, plotType, p):
    #filter out NaN
    new_table = data.loc[data[plotType[3:]] == z].fillna(0)
    #filter out 0 - as they produce inaccurate result in the machine learning
    new_table = new_table[new_table.value != 0]
    # generates the plot # mod.plot(new_table, graphtype, xval, yval, plotval)
    X = new_table[new_table.columns[x]].values.reshape(-1, 1)
    Y = new_table[new_table.columns[y]].values.reshape(-1, 1)
    #train the model
    reg = linear_model.LinearRegression()
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, Y, test_size=0.1)
    # training algorithm
    reg.fit(x_train, y_train)
    # predicting x_test
    predictions = reg.predict(x_test)
    prediction_df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': predictions.flatten()})
    # plots test set values
    plt.scatter(x_test, y_test, label='Test', color='gray')
    # plots best-fit line
    plt.plot(x_test, predictions, label='Regression', color='red')
    future = reg.predict([[p]])
    plt.plot(p, future, 'ro', label=p, color='green')
    plt.title(z)
    plt.xlabel(new_table.columns[x])
    plt.ylabel(new_table.columns[y])
    plt.legend()
    plt.show()