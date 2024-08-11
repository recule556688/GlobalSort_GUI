import os
import shutil
from pathlib import Path
from collections import Counter
from src.config import EXTENSIONS_ALL  # Import the combined extensions dictionary
from src.undo import undo_stack


def get_folder_category(folder_path, extensions):
    file_types = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            ext = ext.lower().strip()  # Normalize extension
            if ext in extensions:
                file_types.append(extensions[ext])

    if file_types:
        most_common_category = Counter(file_types).most_common(1)[0][0]
        return most_common_category
    else:
        return "Divers"


def move_file(file, target_directory):
    try:
        target_directory.mkdir(parents=True, exist_ok=True)
        original_location = file.resolve()
        shutil.move(str(file), str(target_directory / file.name))
        undo_stack.append(
            ("file", str(target_directory / file.name), str(original_location))
        )
        print(
            f"Tracked file move: {file.name} from {original_location} to {target_directory / file.name}"
        )
    except Exception as e:
        print(f"Exception when moving file: {e}")


def move_folder(folder, target_directory):
    try:
        target_directory.mkdir(parents=True, exist_ok=True)
        original_location = folder.resolve()
        shutil.move(str(folder), str(target_directory / folder.name))
        undo_stack.append(
            ("folder", str(target_directory / folder.name), str(original_location))
        )
        print(
            f"Tracked folder move: {folder.name} from {original_location} to {target_directory / folder.name}"
        )
    except Exception as e:
        print(f"Exception when moving folder: {e}")


def sort_directory(
    directory, extensions=EXTENSIONS_ALL
):  # Use EXTENSIONS_ALL as the default
    sorted_folders = set()

    if not directory.exists():
        return False, sorted_folders

    # Sort individual files first
    files = [f for f in directory.iterdir() if f.is_file()]
    for file in files:
        dossier_cible = extensions.get(file.suffix.lower(), "Divers")
        dossier_cible_absolu = directory / dossier_cible
        move_file(file, dossier_cible_absolu)
        sorted_folders.add(str(dossier_cible_absolu))

    # Now sort folders based on their individual contents
    folders = [f for f in directory.iterdir() if f.is_dir()]
    for folder in folders:
        category = get_folder_category(folder, extensions)
        target_directory = directory / category
        if not str(target_directory).startswith(str(folder)):
            move_folder(folder, target_directory)
            sorted_folders.add(str(target_directory))

    return True, sorted_folders
