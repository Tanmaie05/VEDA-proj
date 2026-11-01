# =====================================================
# TASK 9 - STUDENT RECORDS USING PYTHON LISTS
# =====================================================

names = []
marks = []


def add_student():
    name = input("Enter student name: ").strip()

    try:
        mark = float(input("Enter student mark: "))

        if mark < 0 or mark > 100:
            print("❌ Marks must be between 0 and 100.")
            return

        names.append(name)
        marks.append(mark)

        print("✅ Student record added successfully!")

    except ValueError:
        print("❌ Please enter a valid mark.")


def view_students():
    if not names:
        print("\n📋 No student records available.")
        return

    print("\n" + "=" * 45)
    print("           📚 STUDENT RECORDS")
    print("=" * 45)

    for i in range(len(names)):
        print(f"{i + 1}. {names[i]} - {marks[i]} marks")

    print("=" * 45)


def search_student():
    if not names:
        print("\n📋 No student records available.")
        return

    search_name = input("Enter student name to search: ").strip().lower()

    found = False

    for i in range(len(names)):
        if names[i].lower() == search_name:
            print(f"✅ Student found: {names[i]} - {marks[i]} marks")
            found = True
            break

    if not found:
        print("❌ Student not found.")


def sort_students():
    if not names:
        print("\n📋 No student records available.")
        return

    records = list(zip(names, marks))

    records.sort(key=lambda x: x[1], reverse=True)

    print("\n" + "=" * 45)
    print("        📊 STUDENTS SORTED BY MARKS")
    print("=" * 45)

    for i, (name, mark) in enumerate(records, start=1):
        print(f"{i}. {name} - {mark} marks")

    print("=" * 45)


def highest_score():
    if not names:
        print("\n📋 No student records available.")
        return

    highest = max(marks)
    index = marks.index(highest)

    print("\n🏆 Highest Score")
    print(f"Student : {names[index]}")
    print(f"Marks   : {highest}")


def lowest_score():
    if not names:
        print("\n📋 No student records available.")
        return

    lowest = min(marks)
    index = marks.index(lowest)

    print("\n📉 Lowest Score")
    print(f"Student : {names[index]}")
    print(f"Marks   : {lowest}")


def main():

    while True:

        print("\n" + "=" * 50)
        print("       🎓 STUDENT RECORD MANAGEMENT")
        print("=" * 50)

        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Sort Students by Marks")
        print("5. Find Highest Score")
        print("6. Find Lowest Score")
        print("7. Exit")

        print("=" * 50)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            sort_students()

        elif choice == "5":
            highest_score()

        elif choice == "6":
            lowest_score()

        elif choice == "7":
            print("\n👋 Thank you for using Student Record Management!")
            break

        else:
            print("❌ Invalid choice. Please select 1-7.")


main()