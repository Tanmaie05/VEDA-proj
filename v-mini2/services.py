
# services.py

from storage import save_data
from data import services


def display_services():
    """Display all available services."""

    print("\n" + "=" * 55)
    print("             AVAILABLE SERVICES")
    print("=" * 55)

    if not services:
        print("No services found.")
        return

    for service in services:
        print("-" * 55)
        print(f"ID       : {service['id']}")
        print(f"Name     : {service['name']}")
        print(f"Category : {service['category']}")
        print(f"Price    : Rs. {service['price']:.2f}")
        print(f"Status   : {service['status']}")

    print("=" * 55)


def add_service():
    """Add a new service."""

    print("\n--- ADD NEW SERVICE ---")

    name = input("Enter service name: ").strip()
    category = input("Enter category: ").strip()

    if not name or not category:
        print("Error: Service name and category cannot be empty.")
        return

    try:
        price = float(input("Enter service price (Rs.): "))

        if price < 0:
            print("Error: Price cannot be negative.")
            return

    except ValueError:
        print("Error: Please enter a valid numeric price.")
        return

    if any(s["name"].casefold() == name.casefold() for s in services):
        print("A service with this name already exists.")
        return

    new_id = max((s["id"] for s in services), default=0) + 1

    service = {
        "id": new_id,
        "name": name,
        "category": category,
        "price": price,
        "status": "Active"
    }

    services.append(service)
    print(f"Service '{name}' added successfully!")


def search_service():
    """Search services by name or category."""

    keyword = input("\nEnter service name or category: ").strip().casefold()

    if not keyword:
        print("Please enter a search term.")
        return

    matches = [
        service for service in services
        if keyword in service["name"].casefold()
        or keyword in service["category"].casefold()
    ]

    if matches:
        print(f"\nFound {len(matches)} matching service(s):")
        for service in matches:
            print(
                f"ID: {service['id']} | "
                f"{service['name']} | "
                f"{service['category']} | "
                f"Rs. {service['price']:.2f} | "
                f"{service['status']}"
            )
    else:
        print("No matching services found.")


def update_service():
    """Update an existing service."""

    try:
        service_id = int(input("\nEnter service ID to update: "))
    except ValueError:
        print("Error: Service ID must be a number.")
        return

    service = next((s for s in services if s["id"] == service_id), None)

    if service is None:
        print("Service not found.")
        return

    print("Press Enter to keep the existing value.")

    name = input(f"Service name [{service['name']}]: ").strip()
    category = input(f"Category [{service['category']}]: ").strip()
    price_text = input(f"Price [{service['price']}]: ").strip()

    if name:
        duplicate = any(
            s["id"] != service_id
            and s["name"].casefold() == name.casefold()
            for s in services
        )

        if duplicate:
            print("Another service already uses that name.")
            return

    if price_text:
        try:
            price = float(price_text)
            if price < 0:
                print("Error: Price cannot be negative.")
                return
        except ValueError:
            print("Error: Enter a valid numeric price.")
            return
    else:
        price = service["price"]

    if name:
        service["name"] = name

    if category:
        service["category"] = category

    service["price"] = price

    print("Service updated successfully!")


def delete_service():
    """Delete a service by its ID."""

    try:
        service_id = int(input("\nEnter service ID to delete: "))
    except ValueError:
        print("Error: Service ID must be a number.")
        return

    service = next((s for s in services if s["id"] == service_id), None)

    if service is None:
        print("Service not found.")
        return

    confirm = input(
        f"Delete '{service['name']}'? (y/n): "
    ).strip().casefold()

    if confirm == "y":
        services.remove(service)
        print("Service deleted successfully.")
    else:
        print("Deletion cancelled.")


def service_menu():
    """Display the service management menu."""

    while True:
        print("\n" + "=" * 45)
        print("       SERVICE MANAGEMENT MODULE")
        print("=" * 45)
        print("1. View All Services")
        print("2. Add New Service")
        print("3. Search Services")
        print("4. Update Service")
        print("5. Delete Service")
        print("0. Return to Main Menu")
        print("=" * 45)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            display_services()
        elif choice == "2":
            add_service()
        elif choice == "3":
            search_service()
        elif choice == "4":
            update_service()
        elif choice == "5":
            delete_service()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please select 0 to 5.")
