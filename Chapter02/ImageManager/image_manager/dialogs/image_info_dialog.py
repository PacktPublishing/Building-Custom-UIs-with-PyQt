"""Image Manager GUI, Part 2
Custom modeless dialog for displaying image information

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

# Import necessary modules
from PyQt6.QtWidgets import (QLabel, QGroupBox, QDialog, 
    QDialogButtonBox, QVBoxLayout)

class ImageInfoDialog(QDialog):

    def __init__(self, parent, selected_image): 
        """Modeless dialog that displays file information for images"""
        super().__init__(parent) 
        metadata = self.collectImageMetaData(selected_image)

        self.setWindowTitle(f"{metadata['file_name']} Info")

        # Create widgets for displaying information
        image_label = QLabel(f"<b>{metadata['base_name']}</b>")
        date_created = QLabel(f"Created: {metadata['date_created'].toString('MMMM d, yyyy h:mm:ss ap')}")
        image_type = QLabel(f"Type: {metadata['extension']}")
        image_size = QLabel(f"Size: {metadata['size']:,} bytes")
        image_location = QLabel(f"Location: {metadata['file_path']}")
        date_modified = QLabel(f"""Modified: {metadata['last_modified'].toString('MMMM d, yyyy h:mm:ss ap')}""")

        # Organize widgets that display metadata using containers/layouts 
        general_v_box = QVBoxLayout()
        general_v_box.addWidget(image_type)
        general_v_box.addWidget(image_size)
        general_v_box.addWidget(image_location)

        general_group_box = QGroupBox("General:")
        general_group_box.setLayout(general_v_box)

        extra_v_box = QVBoxLayout()
        extra_v_box.addWidget(date_modified)

        extra_group_box = QGroupBox("Extra Info:")
        extra_group_box.setLayout(extra_v_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.button_box.accepted.connect(self.accept)

        # Add a layout to the dialog box
        dialog_v_box = QVBoxLayout()
        dialog_v_box.addWidget(image_label)
        dialog_v_box.addWidget(date_created)    
        dialog_v_box.addWidget(general_group_box)
        dialog_v_box.addWidget(extra_group_box)
        dialog_v_box.addStretch(1)
        dialog_v_box.addWidget(self.button_box)
        self.setLayout(dialog_v_box)
    
    def collectImageMetaData(self, image_info):
        """Collect the metadata for the selected image."""
        base_name = image_info.baseName() # Without extension
        file_name = image_info.fileName() # With extension
        date_created = image_info.birthTime() # Returns QDateTime

        extension = image_info.suffix()
        size = image_info.size() # In bytes
        file_path = image_info.absolutePath() # Doesn't include file name
        last_modified = image_info.lastModified() # Returns QDateTime 

        image_metadata = {
            "base_name": base_name,
            "file_name": file_name, 
            "date_created": date_created,
            "extension": extension,
            "size": size,
            "file_path": file_path,
            "last_modified": last_modified}   
        return image_metadata
