"""GIF and Image Viewer GUI
Question 4 - Set up the GUI's main window

Building Custom UIs with PyQt with Packt Publishing
Chapter 1 - Creating GUIs with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, 
    QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QMovie

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize settings, call functions that define 
        UI elements, and display the main window."""
        self.setMinimumSize(700, 400)
        self.setWindowTitle("GIF and Image Viewer")

        # Set up the main window, menu, and dock widgets
        self.setUpMainWindow()
        self.show() # Display the main window

    def setUpMainWindow(self):
        """Set up the application's main window and widgets."""
        self.movie = QMovie() # Create movie object

        self.media_label = QLabel() # Create label to place images/GIFs on
        self.media_label.setPixmap(QPixmap("icons/image_label.png"))
        self.media_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.media_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())