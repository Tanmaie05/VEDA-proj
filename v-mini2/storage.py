
# storage.py

import json
from pathlib import Path

from data import services, programs, inquiries, service_requests

DATA_DIR = Path(__file__).resolve().parent / "data"

DATA_FILES = {
    "services": DATA_DIR / "services.json",
    "programs": DATA_DIR / "programs.json",
    "inquiries": DATA_DIR / "inquiries.json",
    "service_requests": DATA_DIR / "service_requests.json",
}

COLLECTIONS = {
    "services": services,
    "programs": programs,
    "inquiries": inquiries,
    "service_requests": service_requests,
}


def initialize_storage():
    """Create the data directory and load existing records."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for name, filepath in DATA_FILES.items():
        if not filepath.exists():
            save_data(name)
            continue

        try:
            with filepath.open("r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list):
                print(f"Warning: {filepath.name} must contain a list.")
                continue

            COLLECTIONS[name].clear()
            COLLECTIONS[name].extend(records)

        except (json.JSONDecodeError, OSError) as error:
            print(f"Warning: Could not load {filepath.name}: {error}")
            print("The existing in-memory sample data will be retained.")

    print("Data storage initialized successfully.")


def save_data(name):
    """Save one collection to its corresponding JSON file."""

    if name not in DATA_FILES:
        raise ValueError(f"Unknown data collection: {name}")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    filepath = DATA_FILES[name]
    temporary_file = filepath.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(
                COLLECTIONS[name],
                file,
                indent=4,
                ensure_ascii=False,
            )

        temporary_file.replace(filepath)
        return True

    except (OSError, TypeError, ValueError) as error:
        print(f"Error saving {name}: {error}")

        if temporary_file.exists():
            try:
                temporary_file.unlink()
            except OSError:
                pass

        return False


def save_all_data():
    """Save every collection to JSON."""

    success = True

    for name in DATA_FILES:
        if not save_data(name):
            success = False

    if success:
        print("All records saved successfully.")

    return success
