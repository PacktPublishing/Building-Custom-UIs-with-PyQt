"""Question 4 - QCompleter Example GUI

This example demonstrates how to set up QCompleter to use 
and share a model. There are a number of ways to improve the 
GUI, such as making the selected item/text in the QListView
appear in the QLineEdit or fine-tuning when items are selected
using QCompleter. 

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, 
    QListView, QCompleter, QGroupBox, QVBoxLayout, QAbstractItemView)
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex, QItemSelectionModel
from PyQt6.QtGui import QBrush, QColor

class ListModel(QAbstractListModel):

    def __init__(self, parent=None, data=None):
        super().__init__()
        self.parent = parent
        self.data = data

    def rowCount(self, parent):
        """Provides the number of rows in the model."""
        # Number of rows is equal to number of rows in the CSV file
        return len(self.data)

    def data(self, index, role):
        """Handles how the the items are displayed in the 
        table using roles."""
        if index.isValid():
            # data is the text displayed for every index in the table
            data = self.data[index.row()]
        
        # For displaying the text in the list view
        if role == Qt.ItemDataRole.DisplayRole:
            return data

        # QCompleter by default uses EditRole to query the items for matching 
        if role == Qt.ItemDataRole.EditRole:
            # If an item is located, highlight it using the selection model and 
            # scoll to the item
            self.parent.selectionModel().setCurrentIndex(index, QItemSelectionModel.SelectionFlag.SelectCurrent)
            self.parent.scrollTo(index, QAbstractItemView.ScrollHint.PositionAtCenter)
            return data 

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize settings, call functions that define 
        UI elements, and display the main window.""" 
        self.setWindowTitle("QCompleter Example")
        self.setMinimumSize(500, 400)

        self.setUpMainWindow()
        self.show() 

    def setUpMainWindow(self):
        """Set up the GUI's main window."""
        search_line_edit = QLineEdit()
        search_line_edit.setPlaceholderText("Enter text to search for a word below")

        list_of_words = self.loadWordsFromFile() 

        list_view = QListView()   
        # Create a model instance and pass the list of words to the model
        model = ListModel(list_view, list_of_words)
        list_view.setModel(model)

        # Create QCompleter object that shares the same model as the QListView
        completer = QCompleter(list_of_words)
        completer.setFilterMode(Qt.MatchFlag.MatchStartsWith)
        completer.setModel(model)
        search_line_edit.setCompleter(completer) # Set the completer for the QLineEdit

        # Create a layout and organize all of the objects 
        # into a QGroupBox
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(search_line_edit)
        main_v_box.addWidget(list_view)

        word_group_box = QGroupBox("Keywords")
        word_group_box.setLayout(main_v_box)
        self.setCentralWidget(word_group_box)

    def loadWordsFromFile(self):
        """Returns a list of words from the text file."""
        file_name = "datasets/words.txt"
        words = []
        
        with open(file_name, "r") as f:
            for line in f:  
                words.extend(line.split())
        return words

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
