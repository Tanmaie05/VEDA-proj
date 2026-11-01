
from pathlib import Path
import shutil

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx"],
    "Spreadsheets": [".csv", ".xls", ".xlsx"],
    "Code": [".py", ".java", ".c", ".cpp", ".html", ".css", ".js"],
    "Archives": [".zip", ".rar", ".7z"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"]
}


def get_category(file_path):
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_path = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):
    folder = Path(folder_path).resolve()

    if not folder.exists() or not folder.is_dir():
        raise ValueError("The selected folder does not exist.")

    results = []
    moved_count = 0
    skipped_count = 0

    for item in list(folder.iterdir()):
        if not item.is_file() or item.is_symlink():
            continue

        category = get_category(item)
        destination_folder = folder / category

        try:
            destination_folder.mkdir(exist_ok=True)
            destination = get_unique_path(
                destination_folder / item.name
            )

            shutil.move(str(item), str(destination))

            results.append({
                "filename": item.name,
                "category": category,
                "status": "Organized"
            })

            moved_count += 1

        except OSError:
            results.append({
                "filename": item.name,
                "category": category,
                "status": "Failed"
            })

            skipped_count += 1

    return {
        "results": results,
        "moved_count": moved_count,
        "skipped_count": skipped_count
    }
