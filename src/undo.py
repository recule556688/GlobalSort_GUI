import shutil
import os

undo_stack = []


def undo_all_operations():
    if undo_stack:
        print("Starting to undo all operations...")
        while undo_stack:
            item_type, dest, src = undo_stack.pop()
            print(f"Attempting to move {item_type} {dest} back to {src}")

            try:
                if item_type == "file":
                    # Undo file move
                    if os.path.exists(dest):
                        shutil.move(str(dest), str(src))
                        print(f"Successfully moved file {dest} back to {src}")
                    else:
                        print(f"File {dest} does not exist, cannot undo.")
                elif item_type == "folder":
                    # Undo folder move
                    if os.path.exists(dest):
                        shutil.move(str(dest), str(src))
                        print(f"Successfully moved folder {dest} back to {src}")
                    else:
                        print(f"Folder {dest} does not exist, cannot undo.")
            except Exception as e:
                print(f"Failed to undo operation: {e}")
        print("All operations undone.")
    else:
        print("No operations to undo.")
