from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
import sys


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class IconCheckBoxWidget(QWidget):
    def __init__(self, icon_filename, label_text):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Construct the correct path to the icon file using the correct relative paths
        icon_full_path = resource_path(icon_filename)

        # Load the icon
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_full_path).scaled(
            16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )


        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label)

        # Checkbox with text
        self.checkbox = QCheckBox(label_text)
        layout.addWidget(self.checkbox)

        # Adjust alignment
        icon_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.setLayout(layout)

    def isChecked(self):
        return self.checkbox.isChecked()

    def setChecked(self, state):
        self.checkbox.setChecked(state)
