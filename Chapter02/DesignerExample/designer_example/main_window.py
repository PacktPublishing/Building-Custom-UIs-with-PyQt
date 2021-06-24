"""Qt Designer Example GUI
Question 5 – Demonstrates how to use Qt Designer 
and XML .ui files in PyQt6

Sets up the main window.

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

# Import necessary modules
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDialog
# Import relative modules
from .ui_main_window import Ui_MainWindow
from .dialogs.ui_data_entry_dialog import Ui_Dialog

class DataEntryDialog(QDialog):

    def __init__(self):
        super().__init__()

        # Set up the dialog's interface from Qt Designer
        self.dialog = Ui_Dialog()
        self.dialog.setupUi(self)

        # Set variables for the dialog's QLineEdit widgets
        self.name_line = self.dialog.lineEdit
        self.address_line = self.dialog.lineEdit_2

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize setting and display the main window."""   
        # Set up the user interface from Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # From here, connect signals and slots, interact with the 
        # elements, and more. 
        # Connect to the QPushButton to open the data-entry dialog
        self.ui.pushButton.clicked.connect(self.openDataEntryDialog)

        self.show() # Display the main window

    def openDataEntryDialog(self):
        """Display the data entry dialog."""
        data_dialog = DataEntryDialog()
        response = data_dialog.exec()

        if response == 1: # QDialog.DialogCode.Accepted == 1
            # If both line edits contain text, display successful message 
            # in the status bar
            if data_dialog.name_line.text() != "" and data_dialog.address_line.text() != "":
                self.ui.statusbar.showMessage("Data entered successfully", 4000)
            # Else, let the user know information was missing
            else: 
                self.ui.statusbar.showMessage("Some data missing", 4000)   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())