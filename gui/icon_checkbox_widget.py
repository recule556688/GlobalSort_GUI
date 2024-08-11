from PyQt5.QtWidgets import QWidget, QHBoxLayout, QCheckBox, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class IconCheckBoxWidget(QWidget):
    def __init__(self, icon_path, label_text):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)  # Reduce spacing between icon and checkbox

        # Icon
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path).scaled(
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
