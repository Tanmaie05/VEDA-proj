# =====================================================
# TASK 8 - SIMPLE TO-DO LIST
# =====================================================

tasks = []


def add_task():
    task = input("Enter a task: ").strip()

    if task:
        tasks.append(task)
        print("✅ Task added successfully!")
    else:
        print("❌ Task cannot be empty.")


def view_tasks():
    if not tasks:
        print("\n📋 No tasks available.")
        return

    print("\n" + "=" * 45)
    print("              📋 YOUR TASKS")
    print("=" * 45)

    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

    print("=" * 45)


def update_task():
    view_tasks()

    if not tasks:
        return

    try:
        number = int(input("Enter task number to update: "))

        if 1 <= number <= len(tasks):

            new_task = input("Enter the updated task: ").strip()

            if new_task:
                tasks[number - 1] = new_task
                print("✅ Task updated successfully!")
            else:
                print("❌ Task cannot be empty.")

        else:
            print("❌ Invalid task number.")

    except ValueError:
        print("❌ Please enter a valid task number.")


def remove_task():
    view_tasks()

    if not tasks:
        return

    try:
        number = int(input("Enter task number to remove: "))

        if 1 <= number <= len(tasks):

            removed_task = tasks.pop(number - 1)

            print(f"🗑️ Task removed: {removed_task}")

        else:
            print("❌ Invalid task number.")

    except ValueError:
        print("❌ Please enter a valid task number.")


def main():

    while True:

        print("\n" + "=" * 45)
        print("          📝 SIMPLE TO-DO LIST")
        print("=" * 45)

        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Remove Task")
        print("5. Exit")

        print("=" * 45)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task()

        elif choice == "2":
            view_tasks()

        elif choice == "3":
            update_task()

        elif choice == "4":
            remove_task()

        elif choice == "5":
            print("\n👋 Thank you for using the To-Do List!")
            break

        else:
            print("❌ Invalid choice. Please select 1-5.")


main()