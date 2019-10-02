from PyQt4 import QtCore, QtGui, uic
import pandas as pd
import modules as mod
import sys
import collections

Qt = QtCore.Qt


class PandasModel(QtCore.QAbstractTableModel):
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
    table = pd.DataFrame()
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Main.ui', self)
        self.setWindowTitle("Team 23 Python Data Analyser")

        self.actionImport_CSV.activated.connect(self.importCSV)  #imports the csv to the program
        self.actionMerge_CSV.activated.connect(self.mergeCSV)    #merges another csv with the current one

        self.show()

    def importCSV(self):  # imports csv and displays as table in GUI
        try:
            fileName = mod.openFileLocation(self)
            self.table = mod.fileUpload(fileName)
            self.csvTable.setSortingEnabled(True)
            #self.csvTable.setHorizontalHeaderLabels()
            self.csvTable.setModel(PandasModel(self.table))
            self.csvTable.resizeColumnsToContents()
            self.csvTable.show()

        except Exception as e:
            #display error gui
            print e

    def mergeCSV(self):
        try:
            fileName = mod.openFileLocation(self)
            table2 = mod.fileUpload(fileName)

            if collections.Counter(self.table.columns.values) == collections.Counter(table2.columns.values):
                newTable = pd.concat([self.table, table2])
                newTable = newTable.reset_index(drop=True)
            else:
                newTable = pd.concat([self.table, table2], axis=1)

            self.table = newTable

            self.csvTable.setSortingEnabled(True)
            self.csvTable.setModel(PandasModel(self.table))
            self.csvTable.resizeColumnsToContents()
            self.csvTable.show()

        except Exception as e:
            #display error gui?
            print e

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
