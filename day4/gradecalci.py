# =====================================================
# TASK 4 - STUDENT GRADE CALCULATOR
# =====================================================

print("=" * 55)
print("           🎓 STUDENT GRADE CALCULATOR")
print("=" * 55)

try:

    # Taking marks for 5 subjects
    subjects = ["Computer Networks", "Data Structures", "Artificial Intelligence", "Machine Learning", "Operating Systems"]

    marks = []

    for subject in subjects:

        mark = float(input(f"Enter marks for {subject} (0-100): "))

        # Validate marks
        if mark < 0 or mark > 100:
            print("❌ Marks must be between 0 and 100.")
            break

        marks.append(mark)

    # Continue only if all subjects are valid
    if len(marks) == len(subjects):

        # Calculate total and percentage
        total = sum(marks)
        percentage = total / len(subjects)

        # Grade calculation
        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 50:
            grade = "D"
        elif percentage >= 40:
            grade = "E"
        else:
            grade = "F"

        print("\n" + "=" * 55)
        print("              📊 STUDENT RESULT")
        print("=" * 55)

        for subject, mark in zip(subjects, marks):
            print(f"{subject:<20}: {mark}")

        print("-" * 55)
        print(f"Total Marks         : {total}/500")
        print(f"Percentage           : {percentage:.2f}%")
        print(f"Grade                : {grade}")

        print("=" * 55)

except ValueError:

    print("\n❌ Invalid input!")
    print("Please enter numeric marks.")