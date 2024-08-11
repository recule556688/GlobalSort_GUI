from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QListWidget,
    QMessageBox,
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


class CustomExtensionsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.config = load_config()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        self.custom_extension_input = QLineEdit()
        layout.addWidget(QLabel("Custom Extension (e.g., .txt):"))
        layout.addWidget(self.custom_extension_input)

        self.custom_category_input = QLineEdit()
        layout.addWidget(QLabel("Category (e.g., Documents):"))
        layout.addWidget(self.custom_category_input)

        # Add Extension Button with Icon
        add_extension_button = QPushButton(
            QIcon(resource_path("asset/custom_extension.png")), "Add Custom Extension"
        )
        add_extension_button.clicked.connect(self.add_custom_extension)
        layout.addWidget(add_extension_button)

        self.extension_list = QListWidget()
        self.refresh_extension_list()
        layout.addWidget(self.extension_list)

        # Add Spacer
        layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        )

        # Remove Extension Button with Icon
        remove_extension_button = QPushButton(
            QIcon(resource_path("asset/cross.png")), "Remove Selected Extension"
        )
        remove_extension_button.clicked.connect(self.remove_selected_extension)
        layout.addWidget(remove_extension_button)

        self.setLayout(layout)

    def add_custom_extension(self):
        extension = self.custom_extension_input.text().strip()
        category = self.custom_category_input.text().strip()
        if extension and category and extension not in self.config["custom_extensions"]:
            self.config["custom_extensions"][extension] = category
            save_config(self.config)
            self.refresh_extension_list()
            self.custom_extension_input.clear()
            self.custom_category_input.clear()
        else:
            QMessageBox.warning(
                self, "Error", "Extension already exists, or inputs are invalid."
            )

    def remove_selected_extension(self):
        selected_items = self.extension_list.selectedItems()
        if selected_items:
            for item in selected_items:
                extension = item.text().split(":")[0]
                del self.config["custom_extensions"][extension]
            save_config(self.config)
            self.refresh_extension_list()
        else:
            QMessageBox.warning(self, "Error", "No extension selected.")

    def refresh_extension_list(self):
        self.extension_list.clear()
        for ext, cat in self.config["custom_extensions"].items():
            self.extension_list.addItem(f"{ext}: {cat}")
