"""Budget Tracker GUI
Demonstration of customizing a model class, 
specifically QAbstractTableModel

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import (Qt, pyqtSignal, QModelIndex, 
    QAbstractTableModel)
from PyQt6.QtGui import QBrush, QColor     

class TableModel(QAbstractTableModel):

    values_edited = pyqtSignal()

    def __init__(self, headers=None, data=[["", ""]]):
        super().__init__()
        self._headers = headers
        self._data = data

    def rowCount(self, parent):
        return len(self._data)

    def columnCount(self, parent):
        return len(self._headers)

    def data(self, index, role):
        """ """
        if index.isValid():
            # data is the text displayed for every index in the table
            data = self._data[index.row()][index.column()]

        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            # Use values from _headers to set the text for each table's last row
            if index.row() == len(self._data) - 1 and index.column() == 0:
                if "Money In" in self._headers:
                    return "Total Income"
                if "Money Out" in self._headers:
                    return "Total Expenses"
                if "Money Left Over" in self._headers:
                    return "Income Minus Expenses"
            if index.column() == 1:
                total = 0.0
                for item in self._data:
                    value = float(item[1].replace("$", ""))
                    total += value
                if index.row() == len(self._data) - 1:
                    return f"${total:.2f}"
                self.values_edited.emit() # Initialize the values in the beginning 
            return data

        if role == Qt.ItemDataRole.TextAlignmentRole and index.column() == 1:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

        if role == Qt.ItemDataRole.BackgroundRole and index.row() == len(self._data) - 1:
            grey_bg = QBrush(QColor("#C5CDD4"))
            return grey_bg 

    def flags(self, index):
        """ """
        if index.row() == len(self._data) - 1:
            return Qt.ItemFlag.ItemIsEnabled 
        else:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable

    def setData(self, index, value, role):
        """ """
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def headerData(self, section, orientation, role):
        """ """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]

        if role == Qt.ItemDataRole.BackgroundRole:
                blue_bg = QBrush(QColor("#6EEEF8"))
                return blue_bg            

    def insertRows(self, row, count, parent): 
        """ """
        self.beginInsertRows(QModelIndex(), row, row)
        self._data.append(["", "$0.00"]) # Append a list with 2 strings to _data
        self.values_edited.emit()
        self.endInsertRows()
        self.layoutChanged.emit()
        return True

    def removeRow(self, row, index):
        """ """
        if self._data != [] and index.row() != len(self._data) - 1:
            self._data.pop(row)
        else:
            QMessageBox.information(QApplication.activeWindow(), "No Row Selected",
                "No row selected for deletion.")
        self.values_edited.emit()
        self.layoutChanged.emit()
        return True

    def removeRows(self, parent, first, last):
        """ """
        self.beginRemoveRows(QModelIndex(), first, last)
        # Delete all rows from the table and model
        self._data.clear() 
        self.values_edited.emit()
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True