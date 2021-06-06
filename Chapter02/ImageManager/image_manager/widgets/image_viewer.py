"""Image Manager GUI, Part 2
Custom QListWidget

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import (QMenu, QListWidget, QListView, 
    QAbstractItemView) 
from PyQt6.QtCore import Qt, QSize

class ImageViewerListWidget(QListWidget):

    images_info_list = [] # List that holds QFileInfo instances

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