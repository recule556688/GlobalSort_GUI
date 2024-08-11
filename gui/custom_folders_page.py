from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
    QFileDialog,
    QSpacerItem,
    QSizePolicy,
)
from PyQt5.QtGui import QIcon
from src.config import load_config, save_config
import sys
import os


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class CustomFoldersPage(QWidget):
    def __init__(self):
        super().__init__()

        self.config = load_config()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Add Folder Button with Icon
        add_folder_button = QPushButton(
            QIcon(resource_path("asset/custom_folder.png")), "Add Custom Folder"
        )
        add_folder_button.clicked.connect(self.add_custom_folder)
        layout.addWidget(add_folder_button)

        self.folder_list = QListWidget()
        self.refresh_folder_list()
        layout.addWidget(self.folder_list)

        # Add Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Remove Folder Button with Icon
        remove_folder_button = QPushButton(
            QIcon(resource_path("asset/cross.png")), "Remove Selected Folder"
        )
        remove_folder_button.clicked.connect(self.remove_selected_folder)
        layout.addWidget(remove_folder_button)

        self.setLayout(layout)

    def add_custom_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path and folder_path not in self.config["custom_folders"]:
            self.config["custom_folders"].append(folder_path)
            save_config(self.config)
            self.refresh_folder_list()
        elif not folder_path:
            # User canceled the folder selection, do nothing
            pass
        else:
            QMessageBox.warning(self, "Error", "Folder already exists or invalid path.")

    def remove_selected_folder(self):
        selected_items = self.folder_list.selectedItems()
        if selected_items:
            for item in selected_items:
                folder_path = item.text()
                self.config["custom_folders"].remove(folder_path)
            save_config(self.config)
            self.refresh_folder_list()
        else:
            QMessageBox.warning(self, "Error", "No folder selected.")

    def refresh_folder_list(self):
        self.folder_list.clear()
        for folder in self.config["custom_folders"]:
            self.folder_list.addItem(folder)
