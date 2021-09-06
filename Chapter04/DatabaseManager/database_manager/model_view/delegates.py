"""Database Manager GUI - Custom Delegate Classes

Building Custom UIs with PyQt with Packt Publishing
Chapter 4 - Handling Data with PyQt
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import (QComboBox, QLineEdit, 
    QDateEdit, QStyledItemDelegate) 
from PyQt6.QtCore import Qt
from PyQt6.QtSql import QSqlRelationalDelegate

class SqlRelationalDelegate(QSqlRelationalDelegate):

    def __init__(self, parent=None):
        """ Delegate that handles relational data when also 
        using QSortFilterProxyModel """
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """Create the editor to be displayed when using QSqlRelationalTableModel
        and QSortFilterProxyModel."""
        # Don't allow the first column (primary keys) to be edited 
        if index.column() == 0:
            return None

        # Determine the relation between the primary key and the foreign key
        proxy_model = index.model()
        sql_model = proxy_model.sourceModel()
        table_model = sql_model.relationModel(index.column())
        if table_model:
            self.editor = QComboBox(parent)
            self.editor.setModel(table_model)
            self.editor.setModelColumn(table_model.fieldIndex(sql_model.relation(index.column()).displayColumn()))
            self.editor.setAutoFillBackground(True)
            return self.editor
        else:     
            # If there are no foreign keys     
            return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        """Provide data to the editor."""
        sql_model = index.model().sourceModel()
        table_model = sql_model.relationModel(index.column())
        if table_model:
            value = sql_model.data(index, Qt.ItemDataRole.DisplayRole)
            # Determine the type of the foreign key
            if isinstance(value, int):
                editor.setCurrentIndex(value)
            else:
                editor.setCurrentIndex(editor.findText(value))
        else:
            # If there are no foreign keys 
            return super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        """Return the updated editor with new data value."""
        if not(index.isValid()):
            return

        proxy_model = index.model()
        sql_model = proxy_model.sourceModel()
        table_model = sql_model.relationModel(index.column())
        
        # If the column contains a foreign key, set the data 
        # that should be displayed to the user as well as the 
        # roles for that data
        if table_model:
            current_index = editor.currentIndex() # From the QComboBox
            table_col_index = table_model.fieldIndex(sql_model.relation(index.column()).displayColumn())
            table_edit_index = table_model.fieldIndex(sql_model.relation(index.column()).indexColumn())

            proxy_model.setData(index, table_model.data(table_model.index(current_index, table_col_index), Qt.ItemDataRole.DisplayRole), Qt.ItemDataRole.DisplayRole)
            proxy_model.setData(index, table_model.data(table_model.index(current_index, table_edit_index), Qt.ItemDataRole.EditRole), Qt.ItemDataRole.EditRole)
        else:
            return super().setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        return editor.setGeometry(option.rect)

class DateDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        """ Delegate for editing dates """
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """ """
        editor = QDateEdit(parent, calendarPopup=True)
        editor.setDisplayFormat("yyyy-MM-dd")
        editor.setAutoFillBackground(True)
        return editor

class PhoneDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        """ Delegate for editing phone numbers """
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        """ """
        editor = QLineEdit(parent)
        editor.setInputMask("(999) 999-9999;_")
        editor.setAutoFillBackground(True)
        return editor   

class ReadOnlyDelegate(QStyledItemDelegate):

    def __init__(self, parent=None):
        """ Read-only delegate for tables with no foreign keys """
        super().__init__(parent)   

    def createEditor(self, parent, option, index):
        return None

    def editorEvent(self, event, model, option, index):
        """Reimplement the event handler so that editing 
        cannot be performed at the index in the table."""
        return False