# =====================================================
# TASK 10 - CONTACT BOOK USING DICTIONARIES
# =====================================================

contacts = {}


def add_contact():
    contact_id = input("Enter phone number/contact ID: ").strip()

    if contact_id in contacts:
        print("❌ Contact already exists!")
        return

    name = input("Enter contact name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    print("✅ Contact added successfully!")


def view_contacts():
    if not contacts:
        print("\n📋 No contacts available.")
        return

    print("\n" + "=" * 55)
    print("                 📱 CONTACT BOOK")
    print("=" * 55)

    for contact_id, contact in contacts.items():
        print(f"ID     : {contact_id}")
        print(f"Name   : {contact['name']}")
        print(f"Phone  : {contact['phone']}")
        print(f"Email  : {contact['email']}")
        print("-" * 55)


def search_contact():
    contact_id = input("Enter phone number/contact ID to search: ").strip()

    if contact_id in contacts:
        contact = contacts[contact_id]

        print("\n✅ Contact Found!")
        print(f"ID     : {contact_id}")
        print(f"Name   : {contact['name']}")
        print(f"Phone  : {contact['phone']}")
        print(f"Email  : {contact['email']}")

    else:
        print("❌ Contact not found.")


def update_contact():
    contact_id = input("Enter phone number/contact ID to update: ").strip()

    if contact_id not in contacts:
        print("❌ Contact not found.")
        return

    print("\nEnter new contact information:")

    name = input("Enter name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email: ").strip()

    contacts[contact_id] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    print("✅ Contact updated successfully!")


def delete_contact():
    contact_id = input("Enter phone number/contact ID to delete: ").strip()

    if contact_id in contacts:
        deleted_contact = contacts.pop(contact_id)

        print(f"🗑️ Contact '{deleted_contact['name']}' deleted successfully!")

    else:
        print("❌ Contact not found.")


def main():

    while True:

        print("\n" + "=" * 55)
        print("             📱 SIMPLE CONTACT BOOK")
        print("=" * 55)

        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        print("=" * 55)

        choice = input("Enter your choice: ")

        if choice == "1":
            add_contact()

        elif choice == "2":
            view_contacts()

        elif choice == "3":
            search_contact()

        elif choice == "4":
            update_contact()

        elif choice == "5":
            delete_contact()

        elif choice == "6":
            print("\n👋 Thank you for using Contact Book!")
            break

        else:
            print("❌ Invalid choice. Please select 1-6.")


main()