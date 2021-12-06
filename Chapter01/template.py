"""Template GUI 

Building Custom UIs with PyQt with Packt Publishing
Chapter 1 - Creating GUIs with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import QApplication, QMainWindow
#from PyQt6.QtCore import *
#from PyQt6.QtGui import *

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize settings, call functions that define 
        UI elements, and display the main window."""   
        self.show() # Display the main window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())