
# requests_manager.py

from data import service_requests


VALID_PRIORITIES = ["Low", "Medium", "High", "Urgent"]
VALID_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]


def display_requests(records=None):
    """Display all service requests or a filtered list."""

    if records is None:
        records = service_requests

    print("\n" + "=" * 60)
    print("              SERVICE REQUESTS")
    print("=" * 60)

    if not records:
        print("No service requests found.")
        return

    for request in records:
        print("-" * 60)
        print(f"Request ID  : {request['id']}")
        print(f"Customer    : {request['customer']}")
        print(f"Service     : {request['service']}")
        print(f"Description : {request['description']}")
        print(f"Priority    : {request['priority']}")
        print(f"Status      : {request['status']}")

    print("=" * 60)


def add_request():
    """Register a new service request."""

    print("\n--- REGISTER SERVICE REQUEST ---")

    customer = input("Enter customer name: ").strip()
    service = input("Enter requested service: ").strip()
    description = input("Describe the issue/request: ").strip()

    if not customer or not service or not description:
        print("Error: All fields are required.")
        return

    print("\nPriority options:")
    for number, priority in enumerate(VALID_PRIORITIES, start=1):
        print(f"{number}. {priority}")

    try:
        priority_choice = int(input("Select priority (1-4): "))
    except ValueError:
        print("Error: Enter a number between 1 and 4.")
        return

    if priority_choice not in range(1, len(VALID_PRIORITIES) + 1):
        print("Invalid priority selection.")
        return

    new_id = max((item["id"] for item in service_requests), default=0) + 1

    request = {
        "id": new_id,
        "customer": customer,
        "service": service,
        "description": description,
        "priority": VALID_PRIORITIES[priority_choice - 1],
        "status": "Open"
    }

    service_requests.append(request)

    print(f"\nRequest registered successfully! ID: {new_id}")
    print(f"Priority: {request['priority']}")
    print("Status: Open")


def search_requests():
    """Search requests by customer, service, description, or status."""

    keyword = input(
        "\nEnter customer, service, description, or status: "
    ).strip().casefold()

    if not keyword:
        print("Please enter a search term.")
        return

    matches = [
        item for item in service_requests
        if keyword in item["customer"].casefold()
        or keyword in item["service"].casefold()
        or keyword in item["description"].casefold()
        or keyword in item["status"].casefold()
        or keyword in item["priority"].casefold()
    ]

    display_requests(matches)


def filter_requests():
    """Filter requests by priority or status."""

    print("\n1. Filter by Priority")
    print("2. Filter by Status")

    choice = input("Choose filter: ").strip()

    if choice == "1":
        valid_options = VALID_PRIORITIES
        field = "priority"
    elif choice == "2":
        valid_options = VALID_STATUSES
        field = "status"
    else:
        print("Invalid choice.")
        return

    print("\nAvailable options:")
    for option in valid_options:
        print(f"- {option}")

    selected = input("Enter option: ").strip().casefold()

    if selected not in [option.casefold() for option in valid_options]:
        print("Invalid filter value.")
        return

    matches = [
        item for item in service_requests
        if item[field].casefold() == selected
    ]

    display_requests(matches)


def update_request():
    """Update a request's priority and status."""

    try:
        request_id = int(input("\nEnter request ID to update: "))
    except ValueError:
        print("Error: Request ID must be a number.")
        return

    request = next(
        (item for item in service_requests if item["id"] == request_id),
        None
    )

    if request is None:
        print("Service request not found.")
        return

    print(f"\nCustomer: {request['customer']}")
    print(f"Current priority: {request['priority']}")
    print(f"Current status: {request['status']}")

    print("\nPriority options:")
    for number, priority in enumerate(VALID_PRIORITIES, start=1):
        print(f"{number}. {priority}")

    priority_input = input(
        "New priority (1-4, or Enter to keep current): "
    ).strip()

    if priority_input:
        try:
            priority_choice = int(priority_input)
            if priority_choice not in range(1, len(VALID_PRIORITIES) + 1):
                print("Invalid priority selection.")
                return
        except ValueError:
            print("Priority must be a number.")
            return

        request["priority"] = VALID_PRIORITIES[priority_choice - 1]

    print("\nStatus options:")
    for number, status in enumerate(VALID_STATUSES, start=1):
        print(f"{number}. {status}")

    status_input = input(
        "New status (1-4, or Enter to keep current): "
    ).strip()

    if status_input:
        try:
            status_choice = int(status_input)
            if status_choice not in range(1, len(VALID_STATUSES) + 1):
                print("Invalid status selection.")
                return
        except ValueError:
            print("Status must be a number.")
            return

        request["status"] = VALID_STATUSES[status_choice - 1]

    print("\nService request updated successfully!")


def delete_request():
    """Delete a service request after confirmation."""

    try:
        request_id = int(input("\nEnter request ID to delete: "))
    except ValueError:
        print("Error: Request ID must be a number.")
        return

    request = next(
        (item for item in service_requests if item["id"] == request_id),
        None
    )

    if request is None:
        print("Service request not found.")
        return

    confirm = input(
        f"Delete request #{request_id} for {request['customer']}? (y/n): "
    ).strip().casefold()

    if confirm == "y":
        service_requests.remove(request)
        print("Service request deleted successfully.")
    else:
        print("Deletion cancelled.")


def request_menu():
    """Display the service request management menu."""

    while True:
        print("\n" + "=" * 48)
        print("       SERVICE REQUEST MANAGEMENT")
        print("=" * 48)
        print("1. View All Requests")
        print("2. Register New Request")
        print("3. Search Requests")
        print("4. Filter by Priority or Status")
        print("5. Update Request")
        print("6. Delete Request")
        print("0. Return to Main Menu")
        print("=" * 48)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_requests()
        elif choice == "2":
            add_request()
        elif choice == "3":
            search_requests()
        elif choice == "4":
            filter_requests()
        elif choice == "5":
            update_request()
        elif choice == "6":
            delete_request()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please select 0 to 6.")


if __name__ == "__main__":
    request_menu()
