from PyQt4 import QtCore, QtGui, uic
import pandas as pd
import modules as mod
import sys
import collections
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype, is_float_dtype, is_string_dtype

Qt = QtCore.Qt


class PandasModel(QtCore.QAbstractTableModel):
    """Formats CSV into Pandas Dataframe Object"""

    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return QtCore.QVariant(str(
                    self._data.values[index.row()][index.column()]))
        return QtCore.QVariant()

    def sort(self, Ncol, order):
        try:
            self.layoutAboutToBeChanged.emit()
            self._data = self._data.sort_values(self._data.columns[Ncol], ascending=not order)
            self.layoutChanged.emit()
        except Exception as e:
            print(e)


class MainWindow(QtGui.QMainWindow):
    """Main GUI"""
    table = pd.DataFrame()
    view = pd.DataFrame()

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Main.ui', self)
        self.setWindowTitle("Team 23 Python Data Analyser")

        # add graph types
        self.typeBox.addItem("line")
        self.typeBox.addItem("scatter")
        self.typeBox.addItem("bar")
        self.typeBox.addItem("pie")

        self.actionImport_CSV.activated.connect(self.importCSV)  # imports the csv to the program
        self.actionMerge_CSV.activated.connect(self.mergeCSV)  # merges another csv with the current one
        self.actionExport_CSV.activated.connect(
            self.exportCSV)  # exports current table (after modifications) as a csv file
        self.searchView.pressed.connect(self.searchTable)  # Searches table and displays a view
        self.clearView.pressed.connect(self.clearTableView)  # clears the current search view
        self.generate.clicked.connect(self.displayPlot)  # displays plotted graph according to parameters
        self.show()

    def importCSV(self):
        """Imports CSV and displays as table in GUI"""
        try:
            fileName = mod.openFileLocation(self)
            self.table = mod.fileUpload(fileName)
            self.csvTable.setSortingEnabled(True)
            # self.csvTable.setHorizontalHeaderLabels()
            self.csvTable.setModel(PandasModel(self.table))
            self.csvTable.resizeColumnsToContents()
            self.csvTable.show()

            # clears comboboxes to avoid repeat values when another CSV is imported
            self.xBox.clear()
            self.yBox.clear()
            self.plotBox.clear()

            # populate combobox values
            colVal = 0
            self.plotBox.addItem("None")
            for i in self.table.columns:
                colName = str(colVal) + ". " + i
                self.xBox.addItem(colName)
                self.yBox.addItem(colName)
                self.plotBox.addItem(colName)
                colVal += 1

        except Exception as e:
            # Display error message
            mod.errorGUI(str(e))

    def mergeCSV(self):
        """Merges another CSV with the currently open Pandas Dataframe"""
        try:
            fileName = mod.openFileLocation(self)
            table2 = mod.fileUpload(fileName)

            if collections.Counter(self.table.columns.values) == collections.Counter(table2.columns.values):
                newTable = pd.concat([self.table, table2])
                newTable = newTable.reset_index(drop=True)
            else:
                return ValueError("No matching columns found!")
                # newTable = pd.concat([self.table, table2], axis=1)

            self.table = newTable

            self.csvTable.setSortingEnabled(True)
            self.csvTable.setModel(PandasModel(self.table))
            self.csvTable.resizeColumnsToContents()
            self.csvTable.show()


        except Exception as e:
            # Display error message
            mod.errorGUI(str(e))

    def exportCSV(self):
        """Exports the current Pandas Dataframe (after merges and modifications) as a CSV File"""
        try:
            fileName = mod.saveFileLocation(self)
            self.table.to_csv(fileName, encoding='utf-8', index=False)
        except Exception as e:
            # Display error message
            mod.errorGUI(str(e))

    def searchTable(self):
        """Searches the table and presents the search results as a view"""
        try:
            self.view = self.view.iloc[0:0]
            # search table and generates view
            searchQuery = str(self.search.text())

            if searchQuery == "":
                raise ValueError("Please enter a search query!")

            # creates dictionary to hold the float, int and str values of the query
            queryDict = {'string': searchQuery}
            try:
                queryDict['int'] = int(searchQuery)
                queryDict['float'] = float(searchQuery)
            except:
                queryDict['int'] = 0
                queryDict['float'] = 0.0

            # initialises the view dataframe
            for i in self.table.columns:
                loopQ = ""
                # sets the query datatype according to the type in the column
                if is_numeric_dtype(self.table[i].dtype):
                    loopQ = queryDict['int']
                elif is_string_dtype(self.table[i].dtype):
                    loopQ = queryDict['string']
                elif is_float_dtype(self.table[i].dtype):
                    loopQ = queryDict['float']

                # queries the table to see if it has any matches in the column
                queryBool = self.table[i] == loopQ

                # if there are matches, add the rows to the view otherwise will show no result.
                if self.table[queryBool].empty is False:
                    self.view = pd.concat([self.view, self.table.loc[self.table[i] == loopQ]])
                else:
                    continue

            # displays view
            if not self.view.empty:
                self.csvTable.setSortingEnabled(True)
                self.csvTable.setModel(PandasModel(self.view))
                self.csvTable.resizeColumnsToContents()
                self.csvTable.show()
            else:
                raise ValueError("No Value Found!")

        except Exception as e:
            mod.errorGUI(str(e))

    def clearTableView(self):
        """Resets the View to the original table"""
        self.csvTable.setSortingEnabled(True)
        self.csvTable.setModel(PandasModel(self.table))
        self.csvTable.resizeColumnsToContents()
        self.csvTable.show()

    def displayPlot(self):
        """Displays Visualisation of Data using MatPlotLib"""
        try:
            # retrieve combobox values
            graphtype = str(self.typeBox.currentText())
            xaxis = str(self.xBox.currentText())
            yaxis = str(self.yBox.currentText())
            plotType = str(self.plotBox.currentText())
            xval = int(xaxis[0])
            yval = int(yaxis[0])
            plotNone = None

            def defineplot(x):
                if x == "None":
                    return plotNone
                else:
                    a = int(x[0])
                    return a

            plotval = defineplot(plotType)
            # generates the plot (plot func is under modules)
            mod.plot(self.table, graphtype, xval, yval, plotval)
            plt.show()

        except Exception as e:
            mod.errorGUI(str(e))
            print e


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
