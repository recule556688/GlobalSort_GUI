from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
    QCheckBox,
)
from PyQt5.QtGui import QIcon
from pathlib import Path
from src.utils import sort_directory
from src.config import (
    EXTENSIONS_MUSIC,
    EXTENSIONS_VIDEO,
    EXTENSIONS_IMAGE,
    EXTENSIONS_DOCUMENT,
    EXTENSIONS_DOWNLOAD,
    EXTENSIONS_ALL,
    load_config,
)
from .icon_checkbox_widget import IconCheckBoxWidget  # Import the custom widget
import sys
import os

def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

directories_name = {
    "Music": "Music",
    "Videos": "Videos",
    "Images": "Pictures",
    "Documents": "Documents",
    "Downloads": "Downloads",
}

class SortPage(QWidget):
    def __init__(self, status_bar, result_label):
        super().__init__()
        self.status_bar = status_bar
        self.result_label = result_label
        self.config = load_config()

        self.selected_specific_directory = None  # To store the selected specific folder

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        self.add_sort_checkboxes(layout)

        # Add spacers for better visual separation
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.specific_folder_checkbox = QCheckBox("Sort a Specific Folder")
        self.specific_folder_checkbox.clicked.connect(self.select_specific_directory)
        layout.addWidget(self.specific_folder_checkbox)

        self.custom_folders_checkbox = QCheckBox("Sort All Custom Folders")
        layout.addWidget(self.custom_folders_checkbox)

        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        self.sort_button = QPushButton(QIcon(resource_path("asset/sort.png")), "Sort Selected Files")
        self.sort_button.clicked.connect(self.sort_selected_folders)
        layout.addWidget(self.sort_button)

        self.setLayout(layout)

    def add_sort_checkboxes(self, layout):
        # Create custom icon checkboxes
        self.music_checkbox = IconCheckBoxWidget(
            resource_path("asset/custom_logo_chechbox/music.png"), "Sort Music Files"
        )
        layout.addWidget(self.music_checkbox)

        self.video_checkbox = IconCheckBoxWidget(
            resource_path("asset/custom_logo_chechbox/videos.png"), "Sort Video Files"
        )
        layout.addWidget(self.video_checkbox)

        self.image_checkbox = IconCheckBoxWidget(
            resource_path("asset/custom_logo_chechbox/images.png"), "Sort Image Files"
        )
        layout.addWidget(self.image_checkbox)

        self.document_checkbox = IconCheckBoxWidget(
            resource_path("asset/custom_logo_chechbox/doc.png"), "Sort Document Files"
        )
        layout.addWidget(self.document_checkbox)

        self.download_checkbox = IconCheckBoxWidget(
            resource_path("asset/custom_logo_chechbox/download.png"), "Sort Download Files"
        )
        layout.addWidget(self.download_checkbox)

    def select_specific_directory(self):
        if self.specific_folder_checkbox.isChecked():
            self.selected_specific_directory = QFileDialog.getExistingDirectory(
                self, "Select Directory to Sort"
            )
            if self.selected_specific_directory:
                self.status_bar.showMessage(
                    f"Selected Directory: {self.selected_specific_directory}"
                )
            else:
                self.specific_folder_checkbox.setChecked(False)

    def sort_selected_folders(self):
        sorted_folders = []

        # Handle predefined folders
        if self.music_checkbox.isChecked():
            success, folders = self.sort_specific_folder("Music", EXTENSIONS_MUSIC)
            if success:
                sorted_folders.extend(folders)

        if self.video_checkbox.isChecked():
            success, folders = self.sort_specific_folder("Videos", EXTENSIONS_VIDEO)
            if success:
                sorted_folders.extend(folders)

        if self.image_checkbox.isChecked():
            success, folders = self.sort_specific_folder("Images", EXTENSIONS_IMAGE)
            if success:
                sorted_folders.extend(folders)

        if self.document_checkbox.isChecked():
            success, folders = self.sort_specific_folder(
                "Documents", EXTENSIONS_DOCUMENT
            )
            if success:
                sorted_folders.extend(folders)

        if self.download_checkbox.isChecked():
            success, folders = self.sort_specific_folder(
                "Downloads", EXTENSIONS_DOWNLOAD
            )
            if success:
                sorted_folders.extend(folders)

        # Handle specific folder
        if (
            self.specific_folder_checkbox.isChecked()
            and self.selected_specific_directory
        ):
            directory = Path(self.selected_specific_directory)
            success, folders = sort_directory(
                directory, {**EXTENSIONS_ALL, **self.config["custom_extensions"]}
            )
            if success:
                sorted_folders.extend(folders)

        # Handle custom folders
        if self.custom_folders_checkbox.isChecked():
            for folder_path in self.config["custom_folders"]:
                directory = Path(folder_path)
                success, folders = sort_directory(
                    directory, {**EXTENSIONS_ALL, **self.config["custom_extensions"]}
                )
                if success:
                    sorted_folders.extend(folders)

        if sorted_folders:
            self.status_bar.showMessage("Sorting completed!", 5000)
            self.result_label.setText("Sorted Folders:\n" + "\n".join(sorted_folders))
        else:
            self.status_bar.showMessage("No folders selected for sorting.", 5000)

    def sort_specific_folder(self, folder_type, extensions):
        directory = Path.home() / directories_name[folder_type]
        success, sorted_folders = sort_directory(directory, extensions)
        return success, sorted_folders
