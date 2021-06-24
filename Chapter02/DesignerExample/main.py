"""Qt Designer Example GUI
Question 5 – Demonstrates how to use Qt Designer 
and XML .ui files in PyQt6

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

import sys
from PyQt6.QtWidgets import QApplication
from designer_example.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())