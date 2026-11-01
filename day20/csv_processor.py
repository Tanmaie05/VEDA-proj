
import csv


def process_csv(file_path):
    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The CSV file is empty or has no header.")

        required = {"Employee ID", "Name", "Department", "Salary"}

        if not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                "CSV must contain: Employee ID, Name, Department, Salary."
            )

        records = []
        skipped_rows = 0

        for row in reader:
            try:
                name = (row.get("Name") or "").strip()
                department = (row.get("Department") or "").strip()
                employee_id = (row.get("Employee ID") or "").strip()
                salary_text = (row.get("Salary") or "").strip()

                if not name or not department or not employee_id:
                    skipped_rows += 1
                    continue

                salary = float(salary_text)

                if salary < 0:
                    skipped_rows += 1
                    continue

                records.append({
                    "Employee ID": employee_id,
                    "Name": name,
                    "Department": department,
                    "Salary": salary
                })

            except (ValueError, TypeError):
                skipped_rows += 1

    if not records:
        raise ValueError("No valid employee records were found.")

    salaries = [record["Salary"] for record in records]

    return {
        "records": records,
        "employee_count": len(records),
        "total_salary": sum(salaries),
        "average_salary": sum(salaries) / len(salaries),
        "highest_salary": max(salaries),
        "lowest_salary": min(salaries),
        "skipped_rows": skipped_rows
    }