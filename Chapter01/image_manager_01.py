"""Image Manager GUI, Part 1
Sets up the main window and menu bar

Building Custom UIs with PyQt with Packt Publishing
Chapter 1 - Creating GUIs with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMenu, QLabel, 
    QDockWidget, QListWidget, QListView, QAbstractItemView, QScrollArea)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence

class ImageViewerListWidget(QListWidget):

    def __init__(self, parent):
        """Subclassed QListWidget that displays images"""
        super().__init__(parent)
        self.parent = parent
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)

        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setGridSize(QSize(110, 110))
        self.setLayoutMode(QListView.LayoutMode.Batched)
        self.setBatchSize(20) # Default is 100 

        # Methods handling item selection and drag/drop 
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)  

    def contextMenuEvent(self, event):
        """A simple context menu for managing images."""
        context_menu = QMenu(self) # Create menu instance
        context_menu.addAction(self.parent.sort_ascend_act)
        context_menu.addAction(self.parent.sort_descend_act)
        context_menu.addSeparator()
        context_menu.addAction(self.parent.delete_act)
        context_menu.exec(self.mapToGlobal(event.pos()))       

class MainWindow(QMainWindow):

    def __init__(self):
        """MainWindow Constructor for Image Manager"""
        super().__init__() # Constructor for QMainWindow
        self.initializeUI()
        
    def initializeUI(self):
        """Set up the GUI's main window."""
        self.setWindowTitle("Image Manager")
        self.setObjectName("ImageManager")
  
        # Set up the main window, menu, and dock widgets
        self.setUpMainWindow()
        self.displayImagePreviewDock()
        self.createActions()
        self.createMenus()
        self.show() # Display the main window

    def setUpMainWindow(self):
        """Set up the application's main window containing the QListWidget."""
        self.image_view_lw = ImageViewerListWidget(self)
        self.setCentralWidget(self.image_view_lw)

    def createActions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.import_act = QAction("Import Images...", self, triggered=self.importImages)
        self.import_act.setShortcut("Ctrl+I") 

        self.preferences_act = QAction("Preferences...", self, triggered=self.showPreferencesDialog)
           
        self.quit_act = QAction("Quit Task Manager", self, triggered=self.close)
        self.quit_act.setShortcut(QKeySequence.StandardKey.Quit) # Ctrl+Q

        # Create actions for Edit menu
        self.select_all_act = QAction("Select All", self, triggered=self.image_view_lw.selectAll)
        self.select_all_act.setShortcut(QKeySequence.StandardKey.SelectAll) # Ctrl+A

        self.delete_act = QAction("Delete Images", self, triggered=self.deleteImages)
        self.delete_act.setShortcut(QKeySequence.StandardKey.Delete) # Del
        self.delete_act.setEnabled(False)

        # Create actions for View menu
        # Handle the visibility of the dock widget
        self.show_dock_act = self.image_preview_dock.toggleViewAction()
        self.show_dock_act.setText("Show Image View") 

        self.sort_ascend_act = QAction("Sort Ascending", self, 
            triggered=lambda: self.sortListItems(Qt.SortOrder.AscendingOrder))
        self.sort_ascend_act.setEnabled(False)

        self.sort_descend_act = QAction("Sort Descending", self, 
            triggered=lambda: self.sortListItems(Qt.SortOrder.DescendingOrder))
        self.sort_descend_act.setEnabled(False)

        self.fullscreen_act = QAction("Show Fullscreen", self, 
            triggered=self.displayFullScreen, checkable=True)

        # Create actions for Help menu
        self.about_act = QAction("About Image Manager", 
            self, triggered=self.showAboutDialog)

    def createMenus(self):
        """Create the application's menu."""
        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.import_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.preferences_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_act)

        self.edit_menu = self.menuBar().addMenu("&Edit")
        self.edit_menu.addAction(self.select_all_act)
        self.edit_menu.addSeparator()
        self.edit_menu.addAction(self.delete_act)  

        self.view_menu = self.menuBar().addMenu("&View")
        self.view_menu.addAction(self.show_dock_act)  
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.sort_ascend_act)
        self.view_menu.addAction(self.sort_descend_act)
        self.view_menu.addSeparator()
        self.view_menu.addAction(self.fullscreen_act) 

        self.help_menu = self.menuBar().addMenu("&Help")
        self.help_menu.addAction(self.about_act)  

    def displayImagePreviewDock(self):
        """Dock widget that displays a selected image in a scrollable 
        area and uses its file name as the dock's title."""        
        self.image_preview_dock = QDockWidget()
        self.image_preview_dock.setObjectName("PreviewDock")
        self.image_preview_dock.setWindowTitle("Show Image View")
        self.image_preview_dock.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)

        self.display_image_label = QLabel()
        self.display_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.view_scroll_area = QScrollArea()
        self.view_scroll_area.setMinimumWidth(300)
        self.view_scroll_area.setWidgetResizable(True)

        self.image_preview_dock.setWidget(self.view_scroll_area)
        # Set initial location of dock widget
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.image_preview_dock)  

    def displayFullScreen(self, state):
        """Check the state of checkable fullscreen_act. If True, show the 
        main window as fullscreen."""
        if state: self.showFullScreen()
        else: self.showNormal()

    def importImages(self):
        """Placeholder method."""
        pass

    def deleteImages(self):
        """Placeholder method."""
        pass

    def showPreferencesDialog(self):
        """Placeholder method."""
        pass

    def showAboutDialog(self):
        """Placeholder method."""
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())