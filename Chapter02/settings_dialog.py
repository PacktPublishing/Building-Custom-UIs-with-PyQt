"""Settings Manager Dialog 
Question 6 – Create the main window and Settings dialog

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
    QRadioButton, QLineEdit, QTextEdit, QDialog, QDialogButtonBox, 
    QColorDialog, QFrame, QVBoxLayout, QFormLayout)
from PyQt6.QtCore import QSysInfo
from PyQt6.QtGui import QAction

class HorizontalSeparator(QFrame):

    def __init__(self):
        """ Horizontal line for separating widgets in the SettingsDialog """
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Raised)

class SettingsDialog(QDialog):

    def __init__(self):
        """ Dialog to manage the settings of the application """
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(310, 250)

        # Create the general settings widgets for managing the text color, 
        # text alignment, and author of the app's content 
        # NOTE: Altering the default CSS attributes, such as the color, of a 
        # widget can change its appearance. Hence, the button may appear
        # rectangular depending upon your platform
        self.text_color_button = QPushButton()
        self.text_color_button.setStyleSheet("background-color: #000000") # Black
        self.text_color_button.clicked.connect(self.selectTextColor)        

        self.align_left = QRadioButton(text="Left") # Default
        self.align_left.setChecked(True)
        self.align_center = QRadioButton(text="Center")
        self.align_center.setChecked(False)
        self.align_right = QRadioButton(text="Right")
        self.align_right.setChecked(False)

        # Layout and container for alignment radio buttons
        align_v_box = QVBoxLayout()
        align_v_box.setContentsMargins(0,5,0,0)
        align_v_box.addWidget(self.align_left)
        align_v_box.addWidget(self.align_center)
        align_v_box.addWidget(self.align_right)

        align_frame = QFrame()
        align_frame.setFrameShape(QFrame.Shape.NoFrame)
        align_frame.setLayout(align_v_box)

        self.author_name = QLineEdit()
        self.author_name.setMinimumWidth(160)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        dialog_layout = QFormLayout()
        dialog_layout.addRow("<b>Text Color:</b>", self.text_color_button)
        dialog_layout.addRow(HorizontalSeparator())
        dialog_layout.addRow("<b>Text Alignment:</b>", align_frame)
        dialog_layout.addRow(HorizontalSeparator())
        dialog_layout.addRow("<b>Author:</b>", self.author_name)
        dialog_layout.addWidget(self.button_box)
        self.setLayout(dialog_layout)

    def selectTextColor(self):
        """Change the background color of the QPushButton to reflect the
        selected color. This is used to set the text color of the main window's QLineEdit."""
        color = QColorDialog.getColor() # Returns QColor object
        # Use color.name() to get the color in the format "#RRGGBB"
        self.text_color_button.setStyleSheet(f"background-color: {color.name()}")

class MainWindow(QMainWindow):

    def __init__(self):
        """ MainWindow Constructor """
        super().__init__()
        self.initializeUI()
        
    def initializeUI(self):
        """Initialize settings, call methods that define UI elements,
        and display the main window."""  
        self.setUpMainWindow()
        self.createActions()
        self.createMenus() 
        self.show() # Display the window

    def setUpMainWindow(self):
        """Set up the application's main window."""       
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

    def createActions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.settings_act = QAction("Settings...", self, triggered=self.showSettingsDialog)

    def createMenus(self):
        """Create the application's menu."""
        if QSysInfo.productType() == "macos" or "osx":
            self.menuBar().setNativeMenuBar(False)

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.settings_act)

    def showSettingsDialog(self):
        """Display the application's settings dialog."""
        settings_dialog = SettingsDialog()
        settings_dialog.exec() # Create a modal dialog with exec() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
