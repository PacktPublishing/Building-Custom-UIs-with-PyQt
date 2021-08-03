"""Budget Tracker GUI
Demonstration of customizing a delegate class
to display a QDoubleSpinBox editor

Building Custom UIs with PyQt with Packt Publishing
Chapter 3 - Getting More Out of PyQt’s Model/View Programming
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import QDoubleSpinBox, QStyledItemDelegate
from PyQt6.QtCore import Qt

class IncomeSpinBox(QStyledItemDelegate):

    def __init__(self):
        """ Custom delegate with a QDoubleSpinBox editor """
        super().__init__()

    # The following functions are reimplemented to manage the editor widget
    def createEditor(self, parent, option, index):
        """Create the editor widget that will appear at index."""
        editor = QDoubleSpinBox(parent) # Create the editor widget
        editor.setDecimals(2) 
        editor.setPrefix("$")
        editor.setRange(0.00, 100000.00)
        editor.setAlignment(
            Qt.AlignmentFlag.AlignRight) # Align the text of the editor widget
        editor.setAutoFillBackground(True)
        return editor

    def setEditorData(self, editor, index):
        """Provide the widget and data to edit."""
        # Get the current item's value from the model at the 
        # selected index
        value = index.model().data(
            index, Qt.ItemDataRole.EditRole)
        new_value = editor.valueFromText(value)
        editor.setValue(new_value)

    def setModelData(self, editor, model, index):
        """Return the updated editor with new data value."""
        value = editor.value()
        new_value = editor.textFromValue(value)
        dollar_value = f"${new_value}"           
        model.setData(index, dollar_value, 
                      Qt.ItemDataRole.EditRole)     

    def updateEditorGeometry(self, editor, option, index):
        """Set the editor's geometry with respect to the view.""" 
        editor.setGeometry(option.rect)