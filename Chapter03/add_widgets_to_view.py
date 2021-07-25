"""Question 5 - Demonstrate how to add widgets into table views

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
    QLabel, QPushButton, QDateEdit, QTableView, QMessageBox,
    QHeaderView, QHBoxLayout, QVBoxLayout, QAbstractItemView)
from PyQt6.QtCore import Qt, QDate, QModelIndex
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem

class EditCellWidget(QWidget):

    def __init__(self, table_view):
        """ A simple class that inherits QWidget and acts as a container 
        for items added to QTableView cells """
        super().__init__()
        self.table_view = table_view
        self.setAutoFillBackground(True) # Prevent the background from showing when editing

        view_button = QPushButton(QIcon("icons/view.png"), None)
        view_button.clicked.connect(self.displayItemValues)
        delete_button = QPushButton(QIcon("icons/trash.png"), None)
        delete_button.clicked.connect(self.deleteTableRows)

        # Create the layout for the buttons
        cell_layout = QHBoxLayout()
        cell_layout.setContentsMargins(0, 0, 0, 0)
        cell_layout.setSpacing(0)
        cell_layout.addWidget(view_button)
        cell_layout.addWidget(delete_button)
        self.setLayout(cell_layout)

    def displayItemValues(self):
        """Simple method that demonstrates how to retrieve the values 
        from the widgets."""
        # Get the model index of the item (in this case the view_button) 
        # at the viewport coordinates 
        index = self.table_view.indexAt(self.pos()) # Get the index of the button pushed
        row = index.row() # Get the row of that button
        # Use the row value to get the index of the cells in that row, column 1
        widget_index = self.table_view.model().sibling(row, 1, QModelIndex()) 
        # Use indexWidget to get the QDateEdit widget
        date_edit_widget = self.table_view.indexWidget(widget_index)
        
        # Get value from the cell in column 0 for the selected row
        name = self.table_view.model().sibling(row, 0, QModelIndex()).data()

        # Display name and date in a QMessageBox
        QMessageBox.information(self, "User Information",
            f"""Name: {name}<br>
            <b>Birthdate: </b>{date_edit_widget.date().toString("MM/dd/yyyy")}""")

    def deleteTableRows(self):
        """Method that demonstrates how to delete the rows from the table."""
        # Get the model index of the item (in this case the delete_button) 
        # at the viewport coordinates 
        index = self.table_view.indexAt(self.pos())
        row = index.row()
        self.table_view.model().removeRow(row)

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize settings, call functions that define 
        UI elements, and display the main window."""  
        self.setWindowTitle("Adding Widgets to QTableView Cells")
        self.setMinimumSize(500, 400)
 
        self.setUpMainWindow()
        self.show() # Display the main window

    def setUpMainWindow(self):
        """Set up the GUI's main window."""
        header_label = QLabel("List of Users")

        # Create model and table objects
        model = QStandardItemModel()
        model.setColumnCount(3)
        model.setHorizontalHeaderLabels(["Name", "Birthdate", "Actions"])

        table_view = QTableView()
        table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # NOTE: Uncomment for table cells to be unselectable
        #table_view.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

        names_list = ["Willman, Joshua", "Davis, Scott", "Garcia, Sky"]

        # Add items to each row in the table by looping over 
        # the names_list and adding the date edit and button widgets
        for row, name in enumerate(names_list):
            model.setItem(row, QStandardItem(name))
            # Setting the widget at an index in a QTableView involves
            # acquiring the QModelIndex values of the current position.
            # One way to do this is to use the QAbstractItemModel.sibling()
            # method to retrieve the QModelIndex index from the specified 
            # row and column (here the column is 1)
            index = table_view.model().sibling(row, 1, QModelIndex())
            date_edit = QDateEdit(QDate.currentDate()) # Create QDateEdit object that starts at current date
            date_edit.setDateRange(QDate(1900, 1, 1), QDate.currentDate())
            date_edit.setDisplayFormat("MM/dd/yyyy")
            date_edit.setAlignment(Qt.AlignmentFlag.AlignRight) # Align the text
            date_edit.setAutoFillBackground(True)
            table_view.setIndexWidget(index, date_edit)
            # Set the widgets in the final column for each row
            index = table_view.model().sibling(row, 2, QModelIndex())
            table_view.setIndexWidget(index, EditCellWidget(table_view))

        # Set up main layout and container object for main window
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(header_label)
        main_v_box.addWidget(table_view)

        container = QWidget()
        container.setLayout(main_v_box)
        self.setCentralWidget(container)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
