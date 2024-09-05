from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QListWidget,
    QStackedWidget,
    QStatusBar,
    QLabel,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
)
from PyQt5.QtGui import QIcon
from .sort_page import SortPage
from .undo_page import UndoPage
from .custom_folders_page import CustomFoldersPage
from .custom_extensions_page import CustomExtensionsPage
from .update_page import UpdatePage
import sys
import os


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 600)

        # Initialize the status bar and result label first
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.result_label = QLabel("Status messages will appear here.")

        self.sidebar_visible = True  # Track sidebar visibility

        self.initUI()

    def initUI(self):
        self.main_layout = QHBoxLayout()

        # Sidebar layout with toggle button on top
        sidebar_layout = QVBoxLayout()

        # Toggle button for sidebar
        self.toggle_button = QPushButton("Hide Sidebar")
        self.toggle_button.setMaximumWidth(120)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        sidebar_layout.addWidget(self.toggle_button)

        # Sidebar navigation with icons
        self.sidebar = QListWidget()
        self.sidebar.addItem(
            QListWidgetItem(QIcon(resource_path("asset/sort.png")), "Sort Options")
        )
        self.sidebar.addItem(
            QListWidgetItem(QIcon(resource_path("asset/undomenu.png")), "Undo Changes")
        )
        self.sidebar.addItem(
            QListWidgetItem(
                QIcon(resource_path("asset/custom_folder.png")), "Custom Folders"
            )
        )
        self.sidebar.addItem(
            QListWidgetItem(
                QIcon(resource_path("asset/custom_extension.png")),
                "Custom Extensions",
            )
        )
        self.sidebar.currentItemChanged.connect(self.display_page)
        sidebar_layout.addWidget(self.sidebar)

        sidebar_layout.addStretch()

        # Add the sidebar layout to the main layout
        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        self.main_layout.addWidget(sidebar_container)

        # Stacked widget to hold different pages
        self.pages = QStackedWidget()
        self.main_layout.addWidget(
            self.pages, 1
        )  # Add stretch factor to make it responsive

        # Add pages
        self.add_pages()

        # Set the central widget
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Set the initial page
        self.sidebar.setCurrentRow(0)

    def add_pages(self):
        self.sort_page = SortPage(self.status_bar, self.result_label)
        self.pages.addWidget(self.sort_page)

        self.undo_page = UndoPage(self.status_bar)
        self.pages.addWidget(self.undo_page)

        self.custom_folders_page = CustomFoldersPage()
        self.pages.addWidget(self.custom_folders_page)

        self.custom_extensions_page = CustomExtensionsPage()
        self.pages.addWidget(self.custom_extensions_page)

    def display_page(self, current, previous):
        self.pages.setCurrentIndex(self.sidebar.row(current))

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.hide()  # Hide the sidebar instead of just setting width to 0
            self.toggle_button.setText("Show Sidebar")
        else:
            self.sidebar.show()  # Show the sidebar again
            self.toggle_button.setText("Hide Sidebar")
        self.sidebar_visible = not self.sidebar_visible
        self.main_layout.update()  # Update layout to reflect changes
