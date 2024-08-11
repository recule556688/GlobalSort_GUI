from PyQt5.QtWidgets import QApplication, QSplashScreen, QLabel
from PyQt5.QtGui import QFont, QPixmap, QMovie, QIcon  # Import QIcon class
from PyQt5.QtCore import Qt, QRect
from gui.main_window import MainWindow
import time

if __name__ == "__main__":
    app = QApplication([])

    # Apply a modern font
    app.setFont(QFont("Segoe UI", 10))

    # Set the application icon
    app.setWindowIcon(QIcon("asset/Tess.png"))  # Path to your .ico or .png file

    window = MainWindow()
    window.setWindowIcon(QIcon("asset/Tess.png"))  # Set the window icon

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
    """
    )

    # Splash screen with logo
    splash = QSplashScreen(QPixmap("asset/Tess.png"))
    splash.show()

    # Add loading spinner below the logo
    spinner_label = QLabel(splash)
    spinner_movie = QMovie("asset/spinner.gif")
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
    window.show()
    splash.finish(window)

    app.exec_()
