"""Budget Tracker GUI
Demonstration of customizing view classes

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import (QPushButton, QTableView, QHeaderView,
    QAbstractItemView, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QModelIndex
# Import relative modules 
from .models import TableModel
from .delegates import IncomeSpinBox

class TableHeaderView(QHeaderView):

    def __init__(self, orientation, parent, title):
        super().__init__(orientation, parent)
        # Create the buttons that will be added to the table headers
        self.add_row_button = QPushButton("+", self)
        # Use the sizeHint() values to determine the height and width 
        # of all of the buttons
        height = self.add_row_button.sizeHint().height()
        width = self.add_row_button.sizeHint().width() + 10
        self.add_row_button.setGeometry(self.offset() + 5, 0, width, height)
        self.add_row_button.clicked.connect(parent.addRowToTable)  

        self.delete_row_button = QPushButton("-", self)
        self.delete_row_button.setGeometry(self.offset() + width + 5, 0, width, height)
        self.delete_row_button.clicked.connect(parent.deleteRowFromTable)

        self.clear_rows_button = QPushButton("Clear", self)
        self.clear_rows_button.setGeometry(self.offset() + width * 2 + 5, 0, width, height)
        self.clear_rows_button.clicked.connect(parent.clearRowsFromTable)

class SpendingsTableView(QTableView):

    # Create class variables for the running total of 
    # the table's second column shared by all instances of the class
    running_totals = ["0.00", "0.00"]
    totals_updated = pyqtSignal(list)

    def __init__(self, headers, data):
        super().__init__()
        self._headers = headers
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        self.model = TableModel(headers, data)
        self.setModel(self.model)
        # Use the built-in QAbstractItemView method scrollToBottom() to 
        # ensure newle added row is immediately visible
        self.model.rowsInserted.connect(self.scrollToBottom)
        self.model.values_edited.connect(self.updateTotalValues)    

        header = TableHeaderView(Qt.Orientation.Horizontal, self, headers)
        self.setHorizontalHeader(header)
        # ... after the _model... relies upon info from the _model...
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().hide()

        # Set the item delegate for a specific column, in this case column 1
        self.setItemDelegateForColumn(1, IncomeSpinBox())

    def addRowToTable(self):
        """Insert an empty row at the end of the ... """
        self.model.insertRows(self.model.rowCount(QModelIndex()), 1, QModelIndex())  

    def deleteRowFromTable(self):  
        """Using the view's selection model, find out which row is
        selected and remove it."""
        if self.selectionModel().hasSelection():
            row = self.selectionModel().currentIndex().row()
            self.model.removeRow(row, self.selectionModel().currentIndex()) 
        else:
            QMessageBox.information(self, "No Row Selected",
                "No row selected for deletion.")

    def clearRowsFromTable(self):
        """ """
        answer = QMessageBox.warning(self, "Clear Table", 
            f"Do you really want to clear the {self._headers[0]} table?",
            QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes,
            QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes:
            # Clear the table and update the Money Left Over table
            self.model.removeRows(self.model.rowCount(QModelIndex()), 0, len(self.model._data))
            self.totals_updated.emit(self.running_totals)
            self.addRowToTable()        
            
    def updateTotalValues(self):
        """ """
        index = self.model.index(len(self.model._data) - 1, 1, QModelIndex())
        if "Money In" in self._headers:
            self.running_totals[0] = index.data()
        elif "Money Out" in self._headers:
            self.running_totals[1] = index.data()
        self.totals_updated.emit(self.running_totals)

class TotalTableView(QTableView):

    def __init__(self, headers):
        super().__init__()   
        # Set the maximum height of the table
        height = self.verticalHeader().minimumSectionSize() # height = 24
        self.setMaximumHeight(height * 2)
     
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)        

        self.model = TableModel(headers=headers, data=[["", "$0.00"]]) 
        self.setModel(self.model) 

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionsClickable(False)
        self.verticalHeader().hide()
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def updateTotalsRow(self, totals_list):
        """ """
        if (totals_list[0] and totals_list[1]) != None:
            income = float(totals_list[0].replace("$", ""))
            expenses = float(totals_list[1].replace("$", ""))
            difference = income - expenses

            remaining = f"${difference:.2f}" # Convert to a string 
            index = self.model.index(0, 1, QModelIndex())
            self.model.setData(index, remaining, Qt.ItemDataRole.EditRole)