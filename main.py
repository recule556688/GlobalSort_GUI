import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtGui import QFont, QPixmap, QMovie, QIcon
from PyQt5.QtCore import Qt, QRect
from gui.main_window import MainWindow


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath("gui")  # Use the current directory

    return os.path.join(base_path, relative_path.replace("\\", "/"))


def get_icon_path():
    """Return the appropriate icon based on the OS"""
    if sys.platform.startswith("linux"):
        return resource_path("asset/folder.png")  # Linux uses .png
    elif sys.platform == "win32":
        return resource_path("asset/folder.ico")  # Windows uses .ico
    elif sys.platform == "darwin":
        return resource_path("asset/folder.png")  # macOS uses .png for icons


if __name__ == "__main__":
    app = QApplication([])

    # Apply a modern font
    app.setFont(QFont("Segoe UI", 12))

    # Set the application icon based on the operating system
    app.setWindowIcon(QIcon(get_icon_path()))

    # Splash screen with logo
    splash = QSplashScreen(QPixmap(get_icon_path()))
    splash.show()

    # Add loading spinner below the logo
    spinner_label = QLabel(splash)
    spinner_movie = QMovie(resource_path("asset/spinner.gif"))
    spinner_label.setMovie(spinner_movie)

    # Position the spinner at the bottom center of the splash screen
    splash_width = splash.size().width()
    spinner_width = 100  # Adjust based on your spinner size
    spinner_label.setGeometry(
        QRect(
            (splash_width - spinner_width) // 2,
            splash.size().height() - 120,
            spinner_width,
            spinner_width,
        )
    )

    spinner_label.setAlignment(Qt.AlignCenter)
    spinner_movie.start()

    # Simulate loading time
    time.sleep(1)

    window = MainWindow()
    window.setWindowTitle("GlobalSort GUI")

    # Apply a custom stylesheet
    app.setStyleSheet(
        """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #3c3f41;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 8px;
            color: #ffffff;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        QCheckBox {
            font-size: 14px;
            color: #ffffff;
        }
        QLabel {
            font-size: 14px;
            color: #ffffff;
        }
        QListWidget {
            background-color: #3c3f41;
            color: #ffffff;
            border: 1px solid #555;
        }
        QLineEdit {
            background-color: #3c3f41;
            border: 1px solid #555;
            padding: 6px;
            color: #ffffff;
        }
        QStatusBar {
            background-color: #3c3f41;
            color: #ffffff;
        }
        QMessageBox {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QMessageBox QLabel {
            color: #ffffff;
        }
        QMessageBox QPushButton {
            background-color: #3c3f41;
            color: #ffffff;
            border: 1px solid #555;
        }
        """
    )
    window.show()
    splash.finish(window)

    app.exec_()
