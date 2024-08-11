import platform
import requests
from pathlib import Path
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
import sys
import os


def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class UpdatePage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_version_file = resource_path("version.txt")
        self.github_api_url = (
            "https://api.github.com/repos/recule556688/GlobalSort_GUI/releases/latest"
        )
        self.root_dir = Path(__file__).resolve().parent

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.description_label = QLabel(
            "Check for updates to ensure you have the latest features and improvements."
        )
        layout.addWidget(self.description_label)

        self.check_updates_button = QPushButton("Check for Updates")
        self.check_updates_button.clicked.connect(self.update_app)
        layout.addWidget(self.check_updates_button)

        self.setLayout(layout)

    def update_app(self):
        try:
            response = requests.get(self.github_api_url)
            response.raise_for_status()
            data = response.json()

            latest_version = data["tag_name"]

            if not Path(self.current_version_file).exists():
                with open(self.current_version_file, "w") as f:
                    f.write("0.0.0")
            with open(self.current_version_file, "r") as f:
                current_version = f.read().strip()

            if self.is_newer_version(latest_version, current_version):
                download_url, file_name = self.get_download_url(data)
                if download_url:
                    self.download_and_replace(download_url, file_name, latest_version)
                    QMessageBox.information(
                        self,
                        "Update Complete",
                        "The application has been updated to the latest version.",
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Update Error",
                        "No suitable update found for your platform.",
                    )
            else:
                QMessageBox.information(
                    self, "No Update", "You are already using the latest version."
                )
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self, "Error", f"Failed to check for updates: {str(e)}"
            )

    def get_download_url(self, data):
        for asset in data["assets"]:
            if platform.system() == "Windows" and asset["name"].endswith(".exe"):
                return asset["browser_download_url"], asset["name"]
            elif platform.system() == "Linux" and not asset["name"].endswith(".exe"):
                return asset["browser_download_url"], asset["name"]
        return None, None

    def download_and_replace(self, url, filename, latest_version):
        response = requests.get(url)
        download_path = Path(filename)
        with open(download_path, "wb") as f:
            f.write(response.content)

        applications_dir = self.root_dir / "Applications"
        applications_dir.mkdir(parents=True, exist_ok=True)

        new_filename = f"GlobalSort_{latest_version}{download_path.suffix}"
        new_path = applications_dir / new_filename

        download_path.replace(new_path)

        with open(self.current_version_file, "w") as f:
            f.write(latest_version)

    @staticmethod
    def is_newer_version(latest_version, current_version):
        latest_parts = list(map(int, latest_version.split(".")))
        current_parts = list(map(int, current_version.split(".")))

        for latest, current in zip(latest_parts, current_parts):
            if latest > current:
                return True
            elif latest < current:
                return False

        return len(latest_parts) > len(current_parts)
