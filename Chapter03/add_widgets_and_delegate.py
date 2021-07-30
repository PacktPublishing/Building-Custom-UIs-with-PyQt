"""Question 7 - Demonstrate how to add widgets and a simple custom 
delegate into table views

NOTE: An error occurs if the user is editing data in the QDateEdit editor 
and hits the Tab key. This is intentionally left out and will be 
covered in the Questions section of Chapter 5, Managing Applications 
with Multiple Windows where we discuss event handling. 

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
    QLabel, QPushButton, QDateEdit, QTableView, QMessageBox,
    QHeaderView, QHBoxLayout, QVBoxLayout, QStyledItemDelegate)
from PyQt6.QtCore import Qt, QDate, QModelIndex
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem

class DateEditDelegate(QStyledItemDelegate):
    
    def __init__(self):
        super().__init__()

    # The following functions are reimplemented to manage the editor widget
    def createEditor(self, parent, option, index):
        """Set up the widget used to edit the item data at the selected index."""
        editor = QDateEdit(parent) # Create the editor widget 
        editor.setDateRange(QDate(1900, 1, 1), QDate.currentDate())
        editor.setDisplayFormat("MM/dd/yyyy")
        editor.setAlignment(Qt.AlignmentFlag.AlignRight) # Align the text of the editor widget
        editor.setAutoFillBackground(True) # Prevent the background from showing when editing
        return editor

    def setEditorData(self, editor, index):
        """Populate the editor widget, which is QDateEdit for this
        example, with data."""
        # Get the current item value from the model at the selected index
        date = index.model().data(index, Qt.ItemDataRole.EditRole) 
        # Convert the string, date, to a QDate object. Using '/' 
        # in the format parameter treats the slashes as text 
        # and not part of the date
        new_date = QDate().fromString(date, "MM'/'dd'/'yyyy")
        editor.setDate(new_date) # Use the QDateTime method setDate() to set the value of the editor

    def setModelData(self, editor, model, index):
        """Update the model with data from the editor, QDateEdit, whenever
        data is entered at the index."""
        # The value of the QDateEdit's date, converted to a string
        date = editor.date().toString("MM'/'dd'/'yyyy") 
        # Use setData() to set the role data for the item at index to value
        model.setData(index, date, Qt.ItemDataRole.EditRole)
        model.setData(index, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, 
                        Qt.ItemDataRole.TextAlignmentRole)

    def updateEditorGeometry(self, editor, option, index):
        """Ensure that the editor is displayed correctly in the view."""
        editor.setGeometry(option.rect)

class EditCellWidget(QWidget):

    def __init__(self, table_view):
        """ A simple class that inherits QWidget and acts as a container 
        for items added to QTableView cells """
        super().__init__()
        self.table_view = table_view
        self.setAutoFillBackground(True)

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
        
        # Get values from the cell in column 0 and 1 for the selected row.
        # The date value can also be easily retrieved since its type is a string
        name = self.table_view.model().sibling(row, 0, QModelIndex()).data()
        date = self.table_view.model().sibling(row, 1, QModelIndex()).data()

        # Display name and date in a QMessageBox
        QMessageBox.information(self, "User Information",
            f"""Name: {name}<br>
            <b>Birthdate: </b>{date}""")

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
        self.setWindowTitle("Creating a Custom Date Edit Delegate")
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
        # NOTE: setEditTriggers() is not used so that the user 
        # can double-click and edit cells
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        # Set the item delegate for a specific column, in this case column 1
        table_view.setItemDelegateForColumn(1, DateEditDelegate())

        names_list = ["Willman, Joshua", "Davis, Scott", "Garcia, Sky"]

        # Add items to each row in the table by looping over 
        # the names_list and adding the date edit and button widgets
        for row, name in enumerate(names_list):
            model.setItem(row, QStandardItem(name))
            # Create an item and set the initial value for the second column. 
            # Here the QDate values are converted to strings to make it easier 
            # to align the text without having to subclass a model class
            date_item = QStandardItem(QDate.currentDate().toString("MM/dd/yyyy"))
            date_item.setTextAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
            model.setItem(row, 1, date_item)
            # Set the widgets in the final column for each row
            index = model.index(row, 2, QModelIndex())
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
