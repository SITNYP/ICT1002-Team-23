import os
import sys
import collections
import time
from PyQt4 import QtCore, QtGui, uic
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_float_dtype, is_string_dtype
import modules as mod
import pdfkit as pdf
import imgkit as img
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

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

    def emailWindow(self):  # function to open up the email window
        os.system('python Email.py')

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('Main.ui', self)
        self.setWindowTitle("Team 23 Python Data Analyser")

        # add graph types
        self.typeBox.addItem("line")
        self.typeBox.addItem("scatter")
        self.typeBox.addItem("bar")
        self.typeBox.addItem("area")

        # links functions to GUI
        self.actionImport_CSV.activated.connect(self.importCSV)  # imports the csv to the program
        self.actionMerge_CSV.activated.connect(self.mergeCSV)  # merges another csv with the current one
        self.actionExport_CSV.activated.connect(
            self.exportCSV)  # exports current table (after modifications) as a csv file
        self.searchView.pressed.connect(self.searchTable)  # Searches table and displays a view
        self.clearView.pressed.connect(self.clearTableView)  # clears the current search view
        self.actionEmail.activated.connect(self.emailWindow)  # os.system('python Email.py')
        self.generate.clicked.connect(self.displayPlot)  # displays plotted graph according to parameters
        self.actionExport_PDF.activated.connect(self.exportPDF)  # exports raw table data file as pdf file
        self.actionExport_PDF_filtered.activated.connect(
            self.exportPDF_filter)  # export filtered table data to pdf file
        self.actionExport_IMG.activated.connect(self.exportIMG)  # export raw table data to IMG(.png) file
        self.actionExport_IMG_filtered.activated.connect(
            self.exportIMG_filter)  # export filtered table data to IMG(.png) file
        self.actionExport_TXT.activated.connect(self.exportTXT)  # export raw table data to TXT file
        self.actionExport_TXT_filtered.activated.connect(
            self.exportTXT_filter)  # export filtered table data to TXT file
        self.xFloat.clicked.connect(self.floatConversion)
        self.yFloat.clicked.connect(self.floatConversion)
        self.show()

    # importing/merge/export
    def importCSV(self):
        """Imports CSV and displays as table in GUI"""
        try:
            #prompts user for file location
            fileName = mod.openFileLocation(self)
            
            #populates dataframe with CSV data
            self.table = mod.fileUpload(fileName)
            
            #enables sorting for table by pressing the headers
            self.csvTable.setSortingEnabled(True)
            
            #sets and shows the table in GUI
            self.csvTable.setModel(PandasModel(self.table))
            self.csvTable.resizeColumnsToContents()
            self.csvTable.show()

            # clears comboboxes to avoid repeat values when another CSV is imported
            self.xBox.clear()
            self.yBox.clear()
            self.plotBox.clear()

            # populate combobox values in visualisation
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
            #prompts user for 2nd dataset and stores it as a separate dataframe
            fileName = mod.openFileLocation(self)
            table2 = mod.fileUpload(fileName)
            
            #if same columns are present, then it will merge with the existing dataframe. otherwise will not allow merging
            if collections.Counter(self.table.columns.values) == collections.Counter(table2.columns.values):
                newTable = pd.concat([self.table, table2])
                newTable = newTable.reset_index(drop=True)
            else:
                return ValueError("No matching columns found!")
            
            #initialises table
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
            fileName = mod.saveFileLocation(self) # if search is valid export with the latest version
            if not self.view.empty:
                self.view.to_csv(fileName, encoding='utf-8', index=False)
                 mod.successGUI()
            else:
                self.table.to_csv(fileName, encoding='utf-8', index=False)
                mod.successGUI()
        except Exception as e:
            # Display error message
            mod.errorGUI(str(e))

    def searchTable(self):
        """Searches the table and presents the search results as a view"""
        try:
            self.view = self.view.iloc[0:0]
            # search table and generates view
            searchQuery = str(self.search.text())
            
            #throws an error if there is no search value
            if searchQuery == "":
                raise ValueError("Please enter a search query!")

            # creates dictionary to hold the float, int and str values of the query
            queryDict = {'string': searchQuery}
            
            #if value can be an integer or float, it will convert accordingly. else it will set a default value of 0.
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
                    queryBool = self.table[i] == loopQ
                elif is_string_dtype(self.table[i].dtype):
                    loopQ = queryDict['string']
                    queryBool = self.table[i].str.contains(loopQ, case=False, regex=True)
                elif is_float_dtype(self.table[i].dtype):
                    loopQ = queryDict['float']
                    queryBool = self.table[i] == loopQ

                # if there are matches, add the rows to the view otherwise will show no result.
                if self.table[queryBool].empty is False:
                    self.view = pd.concat([self.view, self.table.loc[queryBool]])
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

    # graph functions
    def floatConversion(self):
        # converts string values to floats
        xaxis = str(self.xBox.currentText())
        yaxis = str(self.yBox.currentText())
        xval = int(xaxis[0])
        yval = int(yaxis[0])
        if self.xFloat.isChecked():
            mod.convertfloatX(self.table, xval)
        if self.yFloat.isChecked():
            mod.convertfloatY(self.table, yval)
        else:
            return

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

            # set the plot value to be None if no columns are selected
            def defineplot(x):
                if x == "None":
                    return plotNone
                else:
                    a = int(x[0])
                    return a

            plotval = defineplot(plotType)

            # generates the plot
            mod.plot(self.table, graphtype, xval, yval, plotval)

        except Exception as e:
            mod.errorGUI(str(e))
            print e

    def displayRegression(self):

        df_trainx = self.table(x)[:-20]  # takes in training set for x axis, everything exceot last 20 items
        df_testx = self.table(x)[-20:]  # takes in testing set for x axis, last 20 items
        df_trainy = self.table(y)[:-20]  # takes in training set for y axis, everything except last 20 items
        df_testy = self.table(y)[-20:]  # takes in testing set for y axis, last 20 items

        regr = linear_model.LinearRegression()  # defines variable for linear regression to take place
        regr.fit(df_trainx, df_trainy)  # fits coordinates into variable based on training sets
        df_predy = regr.predict(df_testx)  # predict based on test sets

        print('Mean squared error: %.2f' % mean_squared_error(df_testy, df_predy))
        print('Variance score: %.2f' % r2_score(df_testy, df_predy))

        mod.plot(self.table, graphtype, df_testx, df_predy, plotval)  # generates regression line (AI trend prediction)

    # exporting functions
    def exportPDF(self):
        """Exports the current Pandas Dataframe as a PDF File (No modifications is made)"""
        dateTimeFormat = time.strftime("%Y%m%d-%H%M%S")  # Date and Time Format (YYYYMMDD-HHMMSS)
        config = pdf.configuration(
            wkhtmltopdf="wkhtmltopdf\\bin\\wkhtmltopdf.exe")  # where the config file is located at

        try:
            if self.table.empty:
                raise ValueError("There is no data!")
            else:
                self.table.to_html('exportPDF.html')  # convert table data to html

                pdfFileName = 'tablePDF-' + dateTimeFormat + ".pdf"  # name file of the pdf file
                pdf.from_file('exportPDF.html', pdfFileName, configuration=config)  # convert html to pdf file

                os.remove('exportPDF.html')  # delete the html file
                mod.successGUI()  # prompt file downloaded

        except Exception as e:
            mod.errorGUI(str(e))

    def exportPDF_filter(self):
        """Exports the current Pandas Dataframe (after merges and modifications) as a PDF File"""
        dateTimeFormat = time.strftime("%Y%m%d-%H%M%S")  # Date and Time Format (YYYYMMDD-HHMMSS)
        config = pdf.configuration(
            wkhtmltopdf="wkhtmltopdf\\bin\\wkhtmltopdf.exe")  # where the config file is located at

        try:
            if self.view.empty:
                raise ValueError("There is no search data!")
            else:
                self.view.to_html('exportPDF_filter.html')
                pdfFileName = 'tablePDF_filter-' + dateTimeFormat + ".pdf"  # name file of the filter pdf file
                pdf.from_file('exportPDF_filter.html', pdfFileName,
                              configuration=config)  # convert html to filter pdf file
                os.remove('exportPDF_filter.html')  # delete the html file
                mod.successGUI()  # prompt file downloaded

        except Exception as e:
            mod.errorGUI(str(e))

    def exportIMG(self):
        """Exports the current Pandas Dataframe as a IMG(.png) File (No modifications is made)"""
        dateTimeFormat = time.strftime("%Y%m%d-%H%M%S")  # Date and Time Format (YYYYMMDD-HHMMSS)
        config = img.config(wkhtmltoimage="wkhtmltopdf\\bin\\wkhtmltoimage.exe")

        try:
            if self.table.empty:
                raise ValueError("There is no data!")
            else:
                self.table.to_html('exportIMG.html')  # export data to html
                img.from_file("exportIMG.html", "table_image-" + dateTimeFormat + ".png",
                              config=config)  # from html change to img(.png) file
                os.remove('exportIMG.html')  # delete html file
                mod.successGUI()  # prompt file downloaded

        except Exception as e:
            mod.errorGUI(str(e))

    def exportIMG_filter(self):
        """Exports the current Pandas Dataframe (after merges and modifications) as a IMG(.png) File"""
        dateTimeFormat = time.strftime("%Y%m%d-%H%M%S")  # Date and Time Format (YYYYMMDD-HHMMSS)
        config = img.config(wkhtmltoimage="wkhtmltopdf\\bin\\wkhtmltoimage.exe")

        try:
            if self.view.empty:
                raise ValueError("There is no search data!")
            else:
                self.view.to_html('exportIMG_filter.html')
                img.from_file("exportIMG_filter.html", "table_image_filter-" + dateTimeFormat + ".png",
                              config=config)  # from html change to img(.png) file
                os.remove('exportIMG_filter.html')  # delete html file
                mod.successGUI()  # prompt file downloaded

        except Exception as e:
            mod.errorGUI(str(e))

    def exportTXT(self):
        dateTimeFormat = time.strftime("%Y%m%d-%H%M%S")  # Date and Time Format (YYYYMMDD-HHMMSS)
        try:
            if self.table.empty:
                raise ValueError("There is no data!")
            else:
                self.table.to_csv('tableTXT-' + dateTimeFormat + '.TXT', sep='\t')  # export data to TXT file
                mod.successGUI()  # prompt file downloaded

        except Exception as e:
            mod.errorGUI(str(e))

    def exportTXT_filter(self):
        dateTimeFormat = time.strftime("%Y%m%d-%H%M%S")  # Date and Time Format (YYYYMMDD-HHMMSS)

        try:
            if self.view.empty:
                raise ValueError("There is no search data!")
            else:
                self.view.to_csv('tableTXT_filter-' + dateTimeFormat + '.TXT',
                                 sep='\t')  # export filtered data to TXT file
                mod.successGUI()  # prompt file downloaded

        except Exception as e:
            mod.errorGUI(str(e))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
