
import csv
import io
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "student_results_25_students.csv"
JSON_FILE = BASE_DIR / "students.json"
BACKUP_FILE = BASE_DIR / "students_backup.json"

SUBJECTS = [
    "Python",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Mathematics",
]

PASS_MARK = 35
MAX_MARKS = 100



def read_csv_file():
    """Read and validate CSV data using common encodings and delimiters."""

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}\n"
            "Place the CSV file in the same folder as this script."
        )

    raw_data = CSV_FILE.read_bytes()

    if not raw_data.strip():
        raise ValueError("The CSV file is empty.")

    # Detect UTF-16 before trying other encodings.
    if raw_data.startswith((b"\xff\xfe", b"\xfe\xff")):
        content = raw_data.decode("utf-16")
    else:
        content = None
        for encoding in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                content = raw_data.decode(encoding)
                break
            except UnicodeDecodeError:
                continue

        if content is None:
            raise ValueError("Unable to decode the CSV file.")

    # Remove null bytes and normalize line endings.
    content = content.replace("\x00", "")
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # Try common CSV delimiters.
    for delimiter in (",", ";", "\t", "|"):
        try:
            reader = csv.DictReader(
                io.StringIO(content, newline=""),
                delimiter=delimiter,
                strict=True,
            )

            fieldnames = reader.fieldnames

            if not fieldnames:
                continue

            fieldnames = [
                name.strip().lstrip("\ufeff")
                for name in fieldnames
            ]

            # Check whether this delimiter produces separate columns.
            normalized = {
                name.casefold() for name in fieldnames
            }

            expected = {
                "student id",
                "student name",
                "usn",
                "semester",
                *[subject.casefold() for subject in SUBJECTS],
            }

            if len(fieldnames) > 1 and len(normalized & expected) >= 3:
                # Reset and read again using the detected delimiter.
                reader = csv.DictReader(
                    io.StringIO(content, newline=""),
                    delimiter=delimiter,
                    strict=True,
                )

                rows = list(reader)

                cleaned_rows = []
                for row in rows:
                    cleaned_rows.append({
                        (key.strip().lstrip("\ufeff") if key else key): value
                        for key, value in row.items()
                    })

                return cleaned_rows, fieldnames

        except csv.Error:
            continue

    raise ValueError(
        "The file could not be parsed as a valid CSV.\n"
        "Open it in Excel and choose File > Save As > "
        'CSV UTF-8 (Comma delimited) (*.csv).\n'
        f"Expected columns: Student ID, Student Name, USN, Semester, "
        f"{', '.join(SUBJECTS)}"
    )


    # Try common encodings, including UTF-8, Windows CSV,
    # and files saved by spreadsheet applications.
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            content = raw_data.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError("Could not decode the CSV file.")

    # Handle UTF-16 CSV files if the file has a UTF-16 BOM.
    if raw_data.startswith((b"\xff\xfe", b"\xfe\xff")):
        content = raw_data.decode("utf-16")

    # Handle a common Excel CSV delimiter variation.
    sample = content[:4096]

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(io.StringIO(content), dialect=dialect)

    if not reader.fieldnames:
        raise ValueError("The CSV file is empty or has no header row.")

    # Remove whitespace and a possible BOM from column names.
    reader.fieldnames = [
        name.strip().lstrip("\ufeff")
        for name in reader.fieldnames
    ]

    return list(reader), reader.fieldnames


def calculate_result(marks):
    """Calculate total, percentage, grade and pass/fail status."""

    total = sum(marks.values())
    maximum = len(SUBJECTS) * MAX_MARKS
    percentage = round((total / maximum) * 100, 2)

    passed = all(marks[subject] >= PASS_MARK for subject in SUBJECTS)

    if not passed:
        grade = "F"
        status = "Fail"
    else:
        status = "Pass"

        if percentage >= 90:
            grade = "O"
        elif percentage >= 80:
            grade = "A+"
        elif percentage >= 70:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "D"

    return {
        "total": total,
        "maximum": maximum,
        "percentage": percentage,
        "grade": grade,
        "status": status,
    }


def import_students():
    """Import CSV student records and save them as JSON."""

    try:
        rows, columns = read_csv_file()
    except (OSError, ValueError) as error:
        print(f"\nERROR: {error}")
        return

    required_columns = [
        "Student ID",
        "Student Name",
        "USN",
        "Semester",
        *SUBJECTS,
    ]

    missing_columns = [
        column for column in required_columns
        if column not in columns
    ]

    if missing_columns:
        print("\nERROR: Required CSV columns are missing:")
        for column in missing_columns:
            print(f" - {column}")

        print("\nAvailable columns:", columns)
        print(
            "\nCheck the CSV header row. Column names must match "
            "the expected names in this script."
        )
        return

    students = []
    seen_usns = set()
    skipped = 0

    for line_number, row in enumerate(rows, start=2):
        try:
            student_id_text = (row.get("Student ID") or "").strip()
            name = (row.get("Student Name") or "").strip()
            usn = (row.get("USN") or "").strip().upper()
            semester_text = (row.get("Semester") or "").strip()

            if not all([student_id_text, name, usn, semester_text]):
                raise ValueError("Missing student details")

            student_id = int(student_id_text)
            semester = int(semester_text)

            if student_id < 1:
                raise ValueError("Student ID must be positive")

            if not 1 <= semester <= 8:
                raise ValueError("Semester must be between 1 and 8")

            if usn in seen_usns:
                raise ValueError(f"Duplicate USN: {usn}")

            marks = {}

            for subject in SUBJECTS:
                value = (row.get(subject) or "").strip()

                if not value:
                    raise ValueError(f"Missing marks for {subject}")

                mark = float(value)

                if not mark.is_integer():
                    raise ValueError(
                        f"{subject} marks must be a whole number"
                    )

                mark = int(mark)

                if not 0 <= mark <= MAX_MARKS:
                    raise ValueError(
                        f"{subject} marks must be between 0 and 100"
                    )

                marks[subject] = mark

            result = calculate_result(marks)

            student = {
                "id": student_id,
                "name": name,
                "usn": usn,
                "semester": semester,
                "marks": marks,
                **result,
            }

            students.append(student)
            seen_usns.add(usn)

        except (ValueError, TypeError, AttributeError) as error:
            skipped += 1
            print(f"Skipping CSV row {line_number}: {error}")

    if not students:
        print("\nNo valid student records found.")
        print("Existing students.json has not been changed.")
        return

    # Prevent accidentally overwriting a larger existing dataset.
    if JSON_FILE.exists():
        try:
            existing_data = json.loads(
                JSON_FILE.read_text(encoding="utf-8")
            )
        except (json.JSONDecodeError, OSError) as error:
            print(f"\nERROR: Cannot safely read existing JSON: {error}")
            print("Existing file has not been changed.")
            return

        if not isinstance(existing_data, list):
            print("\nERROR: students.json must contain a JSON list.")
            print("Existing file has not been changed.")
            return

        # Make a backup before replacing any existing records.
        try:
            BACKUP_FILE.write_text(
                json.dumps(existing_data, indent=4, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError as error:
            print(f"\nERROR: Could not create backup: {error}")
            print("Existing file has not been changed.")
            return

        print(f"Backup created: {BACKUP_FILE.name}")

    try:
        JSON_FILE.write_text(
            json.dumps(students, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as error:
        print(f"\nERROR: Could not save student records: {error}")
        print("Check file permissions and try again.")
        return

    print("\n" + "=" * 42)
    print(" STUDENT DATA IMPORT COMPLETED")
    print("=" * 42)
    print(f"CSV file       : {CSV_FILE.name}")
    print(f"Records imported: {len(students)}")
    print(f"Records skipped : {skipped}")
    print(f"JSON file saved : {JSON_FILE.name}")
    print("=" * 42)


if __name__ == "__main__":
    import_students()
