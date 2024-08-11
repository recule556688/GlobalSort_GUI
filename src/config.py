# src/config.py
import json
from pathlib import Path

CONFIG_FILE = Path.home() / ".folder_sorter_config.json"

default_config = {"custom_folders": [], "custom_extensions": {}}


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        return default_config.copy()


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


EXTENSIONS_MUSIC = {
    ".mp3": "Musique",
    ".wav": "Musique",
    ".flac": "Musique",
    ".ogg": "Musique",
    ".wma": "Musique",
    ".m4a": "Musique",
    ".aac": "Musique",
    ".aiff": "Musique",
    ".ape": "Musique",
}

EXTENSIONS_VIDEO = {
    ".mp4": "Videos",
    ".avi": "Videos",
    ".gif": "Videos",
    ".mkv": "Videos",
    ".wmv": "Videos",
    ".mov": "Videos",
}

EXTENSIONS_IMAGE = {
    ".bmp": "Images",
    ".png": "Images",
    ".jpg": "Images",
    ".JPG": "Images",
    ".jpeg": "Images",
    ".heic": "Images",
    ".svg": "Images",
}

EXTENSIONS_DOCUMENT = {
    ".txt": "Documents",
    ".pptx": "Documents",
    ".csv": "Documents",
    ".xls": "Documents",
    ".odp": "Documents",
    ".pages": "Documents",
    ".pdf": "Documents",
    ".doc": "Documents",
    ".zip": "Documents",
    ".docx": "Documents",
}

EXTENSIONS_DOWNLOAD = {
    ".exe": "executable",
    ".bat": "executable",
    ".sh": "executable",
    ".py": "executable",
    ".pyw": "executable",
    ".msi": "executable",
    ".apk": "executable",
    ".app": "executable",
    ".deb": "executable",
    ".rpm": "executable",
    ".bin": "executable",
    ".dmg": "executable",
    ".run": "executable",
    ".jar": "executable",
}

EXTENSIONS_PERSONNALISER = {
    ".ttf": "Fonts",
}

# Combine all extensions into a single dictionary for easier access
EXTENSIONS_ALL = {
    **EXTENSIONS_MUSIC,
    **EXTENSIONS_VIDEO,
    **EXTENSIONS_IMAGE,
    **EXTENSIONS_DOCUMENT,
    **EXTENSIONS_DOWNLOAD,
    **EXTENSIONS_PERSONNALISER,
}
