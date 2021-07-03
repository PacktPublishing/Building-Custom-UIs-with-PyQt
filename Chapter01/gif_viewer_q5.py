"""GIF and Image Viewer GUI
Question 5 - Set up the GUI's dock widget

Building Custom UIs with PyQt with Packt Publishing
Chapter 1 - Creating GUIs with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
    QPushButton, QLineEdit, QFrame, QDockWidget, QTreeWidget, 
    QHBoxLayout, QVBoxLayout)
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

        # Set up the main window and dock widget
        self.setUpMainWindow()
        self.displayFilesDock()
        self.show() # Display the main window

    def setUpMainWindow(self):
        """Set up the application's main window and widgets."""
        self.movie = QMovie() # Create movie object

        self.media_label = QLabel() # Create label to place images/GIFs on
        self.media_label.setPixmap(QPixmap("icons/image_label.png"))
        self.media_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.media_label)

    def displayFilesDock(self):
        """Dock widget that displays the movie file location in a QLineEdit 
        widget, provides a button for opening directories with images and GIFs, 
        and shows the media from the selected folder in a QTreeWidget."""
        self.files_dock = QDockWidget()
        self.files_dock.setWindowTitle("Media Folder")
        self.files_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea)

        folder_label = QLabel("Media Location:")
        # The QLineEdit widget is set to read-only as a quick way to display 
        # the folder path
        self.folder_line = QLineEdit()
        self.folder_line.setMinimumWidth(100)
        self.folder_line.setReadOnly(True)

        open_button = QPushButton("Open...")

        folder_h_box = QHBoxLayout()
        folder_h_box.addWidget(folder_label)
        folder_h_box.addWidget(self.folder_line)
        folder_h_box.addWidget(open_button)

        self.files_tree = QTreeWidget()
        self.files_tree.setHeaderLabel("Media Files")
        self.files_tree.setColumnCount(1)

        # Set up the dock's layout
        dock_v_box = QVBoxLayout()
        dock_v_box.addLayout(folder_h_box)
        dock_v_box.addWidget(self.files_tree)

        dock_container = QWidget()
        dock_container.setLayout(dock_v_box)

        self.files_dock.setWidget(dock_container)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.files_dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())