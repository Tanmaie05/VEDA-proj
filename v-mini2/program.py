
# programs.py

from data import programs


def display_programs():
    """Display all available training programs."""

    print("\n" + "=" * 55)
    print("             TRAINING PROGRAMS")
    print("=" * 55)

    if not programs:
        print("No training programs available.")
        return

    for program in programs:
        print("-" * 55)
        print(f"ID       : {program['id']}")
        print(f"Name     : {program['name']}")
        print(f"Duration : {program['duration']}")
        print(f"Category : {program['category']}")
        print(f"Status   : {program['status']}")

    print("=" * 55)


def add_program():
    """Add a new training program."""

    print("\n--- ADD TRAINING PROGRAM ---")

    name = input("Enter program name: ").strip()
    duration = input("Enter duration (e.g. 4 Weeks): ").strip()
    category = input("Enter category: ").strip()

    if not name or not duration or not category:
        print("Error: All fields are required.")
        return

    if any(p["name"].casefold() == name.casefold() for p in programs):
        print("A program with this name already exists.")
        return

    new_id = max((p["id"] for p in programs), default=0) + 1

    new_program = {
        "id": new_id,
        "name": name,
        "duration": duration,
        "category": category,
        "status": "Open"
    }

    programs.append(new_program)
    print(f"Training program '{name}' added successfully!")


def search_program():
    """Search programs by name, duration, or category."""

    keyword = input(
        "\nEnter program name, duration, or category: "
    ).strip().casefold()

    if not keyword:
        print("Please enter a search term.")
        return

    matches = [
        program for program in programs
        if keyword in program["name"].casefold()
        or keyword in program["duration"].casefold()
        or keyword in program["category"].casefold()
    ]

    if not matches:
        print("No matching programs found.")
        return

    print(f"\nFound {len(matches)} program(s):")

    for program in matches:
        print(
            f"ID: {program['id']} | "
            f"{program['name']} | "
            f"{program['duration']} | "
            f"{program['category']} | "
            f"{program['status']}"
        )


def update_program():
    """Update the details of an existing program."""

    try:
        program_id = int(input("\nEnter program ID to update: "))
    except ValueError:
        print("Error: Program ID must be a number.")
        return

    program = next(
        (p for p in programs if p["id"] == program_id),
        None
    )

    if program is None:
        print("Program not found.")
        return

    print("Press Enter to keep the current value.")

    name = input(f"Name [{program['name']}]: ").strip()
    duration = input(f"Duration [{program['duration']}]: ").strip()
    category = input(f"Category [{program['category']}]: ").strip()
    status = input(
        f"Status [{program['status']}] (Open/Closed): "
    ).strip()

    if name and any(
        p["id"] != program_id
        and p["name"].casefold() == name.casefold()
        for p in programs
    ):
        print("Another program already uses that name.")
        return

    if status and status.casefold() not in ("open", "closed"):
        print("Status must be Open or Closed.")
        return

    if name:
        program["name"] = name

    if duration:
        program["duration"] = duration

    if category:
        program["category"] = category

    if status:
        program["status"] = status.title()

    print("Training program updated successfully!")


def delete_program():
    """Delete a training program by ID."""

    try:
        program_id = int(input("\nEnter program ID to delete: "))
    except ValueError:
        print("Error: Program ID must be a number.")
        return

    program = next(
        (p for p in programs if p["id"] == program_id),
        None
    )

    if program is None:
        print("Program not found.")
        return

    confirmation = input(
        f"Delete '{program['name']}'? (y/n): "
    ).strip().casefold()

    if confirmation == "y":
        programs.remove(program)
        print("Training program deleted successfully.")
    else:
        print("Deletion cancelled.")


def program_menu():
    """Display the training program management menu."""

    while True:
        print("\n" + "=" * 45)
        print("     TRAINING PROGRAM MANAGEMENT")
        print("=" * 45)
        print("1. View All Programs")
        print("2. Add New Program")
        print("3. Search Programs")
        print("4. Update Program")
        print("5. Delete Program")
        print("0. Return to Main Menu")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_programs()
        elif choice == "2":
            add_program()
        elif choice == "3":
            search_program()
        elif choice == "4":
            update_program()
        elif choice == "5":
            delete_program()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please select 0 to 5.")


if __name__ == "__main__":
    program_menu()
