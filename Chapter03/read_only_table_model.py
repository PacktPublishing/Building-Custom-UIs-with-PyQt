"""Custom Table Model GUI
Question 3 - Demonstrates how to implement a simple 
custom read-only QAbstractTableModel and how to use roles.

You will notice some lag when resizing the window. 
This issue will be discussed in Chapter 4, Handling Data with PyQt. 

Dataset used in this application can be found at https://data.ny.gov and 
https://data.ny.gov/Recreation/Recommended-Fishing-Rivers-And-Streams/jcxg-7gnm.
License terms are found at https://data.ny.gov/download/77gx-ii52/application/pdf.

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
import sys, csv 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableView, 
    QHeaderView, QAbstractItemView)
from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtGui import QFont, QBrush, QColor

class TableModel(QAbstractTableModel):

    def __init__(self, parent=None, headers=None, data=None):
        super().__init__()
        self.headers = headers
        self.data = data

    def rowCount(self, parent):
        """Provides the number of rows in the model."""
        # Number of rows is equal to number of rows in the CSV file
        return len(self.data)

    def columnCount(self, parent):
        """Provides the number of columns in the model."""
        # Number of columns is equal to number of headers in the CSV file
        return len(self.headers) 

    def data(self, index, role):
        """Handles how the the items are displayed in the 
        table using roles."""
        if index.isValid():
            # data is the text displayed for every index in the table
            data = self.data[index.row()][index.column()]
        
        if role == Qt.ItemDataRole.DisplayRole:
            return data

        # Demonstrates how to set bold text for a specific column
        if role == Qt.ItemDataRole.FontRole and index.column() == 0:
            bold_font = QFont()
            bold_font.setBold(True)
            return bold_font

        # Demonstrates how to set the background color in order to highlight 
        # specific cells that contain desired values
        if role == Qt.ItemDataRole.BackgroundRole and "Brown Trout" in data:
            blue_bg = QBrush(QColor("#6EEEF8"))
            return blue_bg

    def headerData(self, section, orientation, role):
        """Gets the data for each header section from the model.
        This example demonstrates how to set up both the horizontal 
        and vertical headers."""
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                # self.headers is a list. Use list indexing to access
                # the elements and set them for each column header
                return self.headers[section]

            if orientation == Qt.Orientation.Vertical:
                return section # Simply add a section number to each row

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize settings, call functions that define 
        UI elements, and display the main window."""
        self.setWindowTitle("Custom Table Window for Displaying Data")
        self.setMinimumSize(800, 500)

        self.setUpMainWindow()
        self.show()

    def setUpMainWindow(self):
        """Set up the GUI's main window."""
        headers, data = self.loadCSVData()

        # Create QTableView object and set up its behavior
        table_view = QTableView()
        table_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        # Set up the horizontal header so that cells resize to fit
        # contents, and so that the last column stretches to take up empty space
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        table_view.horizontalHeader().setStretchLastSection(True)

        self.model = TableModel(headers=headers, data=data)
        table_view.setModel(self.model)

        self.setCentralWidget(table_view)

    def loadCSVData(self):
        """Load the data from the CSV file.
        Returns the headers and data that will be displayed in the table."""
        file_name = "datasets/recommended-fishing-rivers-and-streams-1.csv"
        data = [] # Holds the data from the file

        with open(file_name, "r") as csv_f:
            reader = csv.reader(csv_f)
            headers = next(reader)
            for i, row in enumerate(csv.reader(csv_f)):
                data.append(row)
        return headers, data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())