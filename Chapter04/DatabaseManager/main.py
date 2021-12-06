"""Database Manager GUI
Entry-point Script

Building Custom UIs with PyQt with Packt Publishing
Chapter 4 - Handling Data with PyQt
Created by: Joshua Willman
"""

import sys
from PyQt6.QtWidgets import QApplication
from database_manager.login import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec())