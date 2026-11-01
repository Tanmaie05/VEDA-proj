
# inquiries.py

from data import inquiries


VALID_STATUSES = ["New", "In Progress", "Resolved"]


def display_inquiries():
    """Display all customer inquiries."""

    print("\n" + "=" * 60)
    print("                 CUSTOMER INQUIRIES")
    print("=" * 60)

    if not inquiries:
        print("No customer inquiries found.")
        return

    for inquiry in inquiries:
        print("-" * 60)
        print(f"ID       : {inquiry['id']}")
        print(f"Customer : {inquiry['customer']}")
        print(f"Subject  : {inquiry['subject']}")
        print(f"Message  : {inquiry['message']}")
        print(f"Status   : {inquiry['status']}")

    print("=" * 60)


def add_inquiry():
    """Register a new customer inquiry."""

    print("\n--- REGISTER CUSTOMER INQUIRY ---")

    customer = input("Enter customer name: ").strip()
    subject = input("Enter inquiry subject: ").strip()
    message = input("Enter inquiry message: ").strip()

    if not customer or not subject or not message:
        print("Error: All fields are required.")
        return

    new_id = max((item["id"] for item in inquiries), default=0) + 1

    inquiry = {
        "id": new_id,
        "customer": customer,
        "subject": subject,
        "message": message,
        "status": "New"
    }

    inquiries.append(inquiry)
    print(f"Inquiry registered successfully! Inquiry ID: {new_id}")


def search_inquiries():
    """Search inquiries by customer name, subject, or status."""

    keyword = input(
        "\nEnter customer name, subject, or status to search: "
    ).strip().casefold()

    if not keyword:
        print("Please enter a search term.")
        return

    matches = [
        item for item in inquiries
        if keyword in item["customer"].casefold()
        or keyword in item["subject"].casefold()
        or keyword in item["status"].casefold()
        or keyword in item["message"].casefold()
    ]

    if not matches:
        print("No matching inquiries found.")
        return

    print(f"\nFound {len(matches)} inquiry/inquiries:")

    for item in matches:
        print("-" * 45)
        print(f"ID: {item['id']}")
        print(f"Customer: {item['customer']}")
        print(f"Subject: {item['subject']}")
        print(f"Message: {item['message']}")
        print(f"Status: {item['status']}")


def update_inquiry_status():
    """Update the status of an inquiry."""

    try:
        inquiry_id = int(input("\nEnter inquiry ID: "))
    except ValueError:
        print("Error: Inquiry ID must be a number.")
        return

    inquiry = next(
        (item for item in inquiries if item["id"] == inquiry_id),
        None
    )

    if inquiry is None:
        print("Inquiry not found.")
        return

    print(f"\nCustomer: {inquiry['customer']}")
    print(f"Current status: {inquiry['status']}")
    print("\nAvailable statuses:")

    for number, status in enumerate(VALID_STATUSES, start=1):
        print(f"{number}. {status}")

    try:
        choice = int(input("Select new status (1-3): "))
    except ValueError:
        print("Error: Enter a number between 1 and 3.")
        return

    if choice not in range(1, len(VALID_STATUSES) + 1):
        print("Invalid status selection.")
        return

    inquiry["status"] = VALID_STATUSES[choice - 1]
    print(f"Inquiry status updated to '{inquiry['status']}'.")


def delete_inquiry():
    """Delete an inquiry after confirmation."""

    try:
        inquiry_id = int(input("\nEnter inquiry ID to delete: "))
    except ValueError:
        print("Error: Inquiry ID must be a number.")
        return

    inquiry = next(
        (item for item in inquiries if item["id"] == inquiry_id),
        None
    )

    if inquiry is None:
        print("Inquiry not found.")
        return

    confirmation = input(
        f"Delete inquiry from {inquiry['customer']}? (y/n): "
    ).strip().casefold()

    if confirmation == "y":
        inquiries.remove(inquiry)
        print("Inquiry deleted successfully.")
    else:
        print("Deletion cancelled.")


def inquiry_menu():
    """Display the customer inquiry management menu."""

    while True:
        print("\n" + "=" * 48)
        print("       CUSTOMER INQUIRY MANAGEMENT")
        print("=" * 48)
        print("1. View All Inquiries")
        print("2. Register New Inquiry")
        print("3. Search Inquiries")
        print("4. Update Inquiry Status")
        print("5. Delete Inquiry")
        print("0. Return to Main Menu")
        print("=" * 48)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_inquiries()
        elif choice == "2":
            add_inquiry()
        elif choice == "3":
            search_inquiries()
        elif choice == "4":
            update_inquiry_status()
        elif choice == "5":
            delete_inquiry()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please select 0 to 5.")


if __name__ == "__main__":
    inquiry_menu()
