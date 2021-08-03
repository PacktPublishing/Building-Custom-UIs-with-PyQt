"""Budget Tracker GUI

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
import os, sys, json
from PyQt6.QtWidgets import (QApplication, QMainWindow, 
    QWidget, QVBoxLayout)
# Import relative modules 
from .model_view.views import SpendingsTableView, TotalTableView

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Set up the GUI's main window."""
        self.setWindowTitle("Budget Tracker GUI")
        self.setMinimumSize(700, 400)        

        self.setUpMainWindow()
        self.show() # Display the main window

    def setUpMainWindow(self):
        """Set up the main window for the budget tracker GUI."""
        self.file_name = "budget_tracker/budget_data.json"
        income, expenses = self.loadBudgetData()

        # Create the 3 tables for displaying the user's income data
        self.income_table = SpendingsTableView(
            headers=["Money In", ""], data=income)
        self.expenses_table = SpendingsTableView(
            headers=["Money Out", ""], data=expenses)
        self.remaining_table = TotalTableView(
            ["Money Left Over", ""])
        self.income_table.totals_updated.connect(
            self.remaining_table.updateTotalsRow)
        self.expenses_table.totals_updated.connect(
            self.remaining_table.updateTotalsRow)

        tables_v_box = QVBoxLayout()
        tables_v_box.addWidget(self.income_table)
        tables_v_box.addWidget(self.expenses_table)
        tables_v_box.addWidget(self.remaining_table)

        self.main_container = QWidget()
        self.main_container.setLayout(tables_v_box)
        self.setCentralWidget(self.main_container)

    def loadBudgetData(self):
        """Load the budget data from a file."""
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as in_file:
                data = json.load(in_file) # Returns dict
                income = data["income"]
                expenses = data["expenses"]
            return income, expenses
        else:
            # Create the file and initiate the tables to start 
            # with a single row if the file does not exist
            with open(self.file_name, "w"):
                return [["", "$0.00"]], [["", "$0.00"]]
    
    def saveBudgetData(self):
        """Save the information in the tables."""
        # Collect the information for both tables by accessing the 
        # _data lists
        income_data = self.income_table.model._data 
        expenses_data = self.expenses_table.model._data

        data = {"income": income_data, 
                "expenses": expenses_data}

        with open(self.file_name, "w") as write_file:
            json.dump(data, write_file)
    
    def closeEvent(self, event):
        """Reimplement closeEvent() to ensure data is saved when 
        closing the window."""
        self.saveBudgetData()
        event.accept()

if __name__ == "__main__":
    # You will need to change the relative import paths if 
    # running the application from here
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())