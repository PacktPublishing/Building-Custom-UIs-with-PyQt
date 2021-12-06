"""GIF and Image Viewer GUI
Question 6 - Set up the GUI's menu bar, menu actions, 
and toolbar

Building Custom UIs with PyQt with Packt Publishing
Chapter 1 - Creating GUIs with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
import sys 
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QLineEdit, QFrame, QDockWidget, QTreeWidget,
    QFileDialog, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import Qt, QSize, QSysInfo
from PyQt6.QtGui import QIcon, QPixmap, QMovie, QAction, QKeySequence

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

        # Set up the main window, menu, and dock widget
        self.setUpMainWindow()
        self.displayFilesDock()
        self.createActions()
        self.createMenus()
        self.createToolbar()
        self.show() # Display the main window

    def setUpMainWindow(self):
        """Set up the application's main window and widgets."""
        self.movie = QMovie() # Create movie object
        self.movie.stateChanged.connect(self.changeButtonStates)

        self.media_label = QLabel() # Create label to place images/GIFs on
        self.media_label.setPixmap(QPixmap("icons/image_label.png"))
        self.media_label.setFrameShape(QFrame.Shape.StyledPanel)
        self.media_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.media_label)

    def createActions(self):
        """Create the application's menu actions."""
        # Create actions for File menu
        self.open_act = QAction("Open...", self, triggered=self.openDirectory)
        self.open_act.setShortcut(QKeySequence.StandardKey.Open) 

        self.quit_act = QAction("Quit Viewer", self, triggered=self.close)
        self.quit_act.setShortcut(QKeySequence.StandardKey.Quit) # Ctrl+Q

        # Create actions for View menu
        # Handle the visibility of the dock widget
        self.show_dock_act = self.files_dock.toggleViewAction()
        self.show_dock_act.setText("Show Media Folder") 

        # Create actions for the toolbar (These actions could also be 
        # added to the GUI's menu bar or to a context menu)
        self.play_act = QAction(QIcon("icons/play.png"), "Play", self, triggered=self.startMovie)
        self.pause_act = QAction(QIcon("icons/pause.png"), "Pause", self, triggered=self.pauseMovie)
        self.stop_act = QAction(QIcon("icons/stop.png"), "Stop/Reset", self, triggered=self.stopMovie)
        self.disableMovieButtons()

    def createMenus(self):
        """Create the application's menu."""
        # Make the toolbar appear in the main window for macOS users.
        # More information about this in Chapter 2 - Building the Foundation for GUIs
        if QSysInfo.productType() == "macos" or "osx":
            self.menuBar().setNativeMenuBar(False)

        self.file_menu = self.menuBar().addMenu("&File")
        self.file_menu.addAction(self.open_act)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_act)

        self.view_menu = self.menuBar().addMenu("&View")
        self.view_menu.addAction(self.show_dock_act)      

    def createToolbar(self):
        """Create the application's toolbar for playing GIFs."""
        toolbar = self.addToolBar("GIF Controls Toolbar")
        toolbar.setIconSize(QSize(24, 24))

        # Add actions to the toolbar
        toolbar.addAction(self.play_act)
        toolbar.addAction(self.pause_act)
        toolbar.addAction(self.stop_act)  

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
        open_button.clicked.connect(self.openDirectory)

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

    def openDirectory(self):
        """Open a QFileDialog for selecting a local directory. Only display 
        image and GIF files.""" 
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory", "", 
            QFileDialog.Option.ShowDirsOnly) # Specify the file mode to only select directories

        if directory:
            self.movie.setFileName(directory)
            # Check if image data is valid before playing
            if self.movie.isValid(): 
                # Use setMovie() to set the label's contents as the selected GIF
                self.media_label.setMovie(self.movie)
                self.startMovie() # Call method to begin playing

    def startMovie(self):
        """Start playing the movie."""
        self.movie.start() 

    def pauseMovie(self):
        """Pause the movie."""
        self.movie.setPaused(True)

    def stopMovie(self):
        """Stop playing the movie and reset the movie back to 
        the first frame."""
        self.movie.stop()
        self.movie.jumpToFrame(0)

    def changeButtonStates(self, state):
        """Slot that handles enabling/disabling buttons in the toolbar
        based on the state of QMovie."""
        if state == QMovie.MovieState.Running:
            # The animation begins playing once control returns to the event loop
            self.play_act.setEnabled(False)
            self.pause_act.setEnabled(True)
            self.stop_act.setEnabled(True)
        if state == QMovie.MovieState.Paused:
            self.play_act.setEnabled(True)
            self.pause_act.setEnabled(False)
            self.stop_act.setEnabled(False)
        if state == QMovie.MovieState.NotRunning:
            self.play_act.setEnabled(True)
            self.pause_act.setEnabled(False)
            self.stop_act.setEnabled(False)

    def disableMovieButtons(self):
        """Simple method to disable the movie buttons in the toolbar."""
        self.play_act.setEnabled(False)
        self.pause_act.setEnabled(False)
        self.stop_act.setEnabled(False)   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())