"""Image Manager GUI, Part 2
Custom Preferences dialog

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import (QLabel, QCheckBox, QGroupBox, 
    QDialog, QDialogButtonBox, QVBoxLayout)

class PreferencesDialog(QDialog):

    def __init__(self, parent, directory, is_checked):
        """Simple modal Preferences dialog"""
        super().__init__(parent)
        self.setWindowTitle("Preferences")
        self.setModal(True)
        
        image_dir_label = QLabel(f"<b>Images Location:</b> {directory.absolutePath()}")

        self.delete_images_checkbox = QCheckBox("Delete Original Images")
        self.delete_images_checkbox.setToolTip("""<p>If checked, images that are copied to the 
            <b>Images Location</b> are also deleted from their original location.</p>""")
        self.delete_images_checkbox.setChecked(is_checked)

        handling_v_box = QVBoxLayout()
        handling_v_box.addWidget(self.delete_images_checkbox)

        handling_group_box = QGroupBox("Image Handling:")
        handling_group_box.setLayout(handling_v_box)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Add a layout to the dialog box
        dialog_v_box = QVBoxLayout()
        dialog_v_box.addWidget(image_dir_label)
        dialog_v_box.addWidget(handling_group_box)
        dialog_v_box.addStretch(1)
        dialog_v_box.addWidget(self.button_box)
        self.setLayout(dialog_v_box)