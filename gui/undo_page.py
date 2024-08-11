from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from src.undo import undo_all_operations


class UndoPage(QWidget):
    def __init__(self, status_bar):
        super().__init__()
        self.status_bar = status_bar

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        undo_button = QPushButton(QIcon("asset/undo.png"), "Undo All Operations")
        undo_button.clicked.connect(self.undo_last_operation)
        layout.addWidget(undo_button)

        self.setLayout(layout)

    def undo_last_operation(self):
        undo_all_operations()
        self.status_bar.showMessage("Last operation undone.", 5000)
