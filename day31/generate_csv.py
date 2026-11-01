
import csv
import random
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent / "student_results_25_students.csv"

SUBJECTS = [
    "Python",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Mathematics",
]

HEADERS = [
    "Student ID",
    "Student Name",
    "USN",
    "Semester",
    *SUBJECTS,
]

FIRST_NAMES = [
    "Aarav", "Aditi", "Arjun", "Ananya", "Rohan",
    "Sneha", "Rahul", "Priya", "Kiran", "Divya",
    "Aditya", "Pooja", "Vikram", "Meera", "Nikhil",
    "Kavya", "Sanjay", "Isha", "Varun", "Neha",
    "Manoj", "Shreya", "Akash", "Pallavi", "Siddharth",
]

LAST_NAMES = [
    "Sharma", "Patil", "Rao", "Kumar", "Shetty",
    "Gowda", "Reddy", "Kulkarni", "Joshi", "Naik",
    "Verma", "Desai", "Hegde", "Mishra", "Singh",
    "Poojary", "Bhat", "Gupta", "Nayak", "Jain",
    "Shah", "Mehta", "Iyer", "Pillai", "Das",
]

random.seed(42)

with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
    writer = csv.DictWriter(file, fieldnames=HEADERS)
    writer.writeheader()

    for student_id in range(1, 26):
        row = {
            "Student ID": student_id,
            "Student Name": (
                f"{FIRST_NAMES[student_id - 1]} "
                f"{LAST_NAMES[student_id - 1]}"
            ),
            "USN": f"1OX23CS{student_id:03d}",
            "Semester": random.randint(3, 7),
        }

        for subject in SUBJECTS:
            row[subject] = random.randint(30, 100)

        writer.writerow(row)

print("\n" + "=" * 42)
print("   STUDENT CSV GENERATED SUCCESSFULLY")
print("=" * 42)
print(f"File: {OUTPUT_FILE.name}")
print("Student records: 25")
print("Subjects: 5")
print("=" * 42)
